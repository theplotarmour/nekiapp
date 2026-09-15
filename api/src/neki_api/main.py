import logging
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from typing import Literal
from uuid import UUID, uuid4

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel, ConfigDict
from starlette.exceptions import HTTPException
from starlette.middleware.cors import CORSMiddleware
from starlette.types import ASGIApp, Message, Receive, Scope, Send

from neki_api.config import Settings
from neki_api.database import Database

logger = logging.getLogger("neki.request")


class RequestContext:
    def __init__(self, app: ASGIApp) -> None:
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return
        raw = dict(scope.get("headers", [])).get(b"x-request-id", b"")
        try:
            request_id = str(UUID(raw.decode("ascii")))
        except (ValueError, UnicodeDecodeError):
            request_id = str(uuid4())
        scope.setdefault("state", {})["request_id"] = request_id
        started = False

        async def send_with_context(message: Message) -> None:
            nonlocal started
            if message["type"] == "http.response.start":
                started = True
                message.setdefault("headers", []).extend(
                    [
                        (b"x-request-id", request_id.encode()),
                        (b"cache-control", b"no-store"),
                        (b"x-content-type-options", b"nosniff"),
                    ]
                )
            await send(message)

        try:
            await self.app(scope, receive, send_with_context)
        except Exception:
            logger.error("request_failed request_id=%s", request_id)
            if started:
                raise
            response = error_response(500, "INTERNAL_ERROR", "Something went wrong.", request_id)
            await response(scope, receive, send_with_context)


class Health(BaseModel):
    model_config = ConfigDict(extra="forbid")
    status: Literal["ok", "ready"]


class ErrorDetails(BaseModel):
    model_config = ConfigDict(extra="forbid")


class ErrorPayload(BaseModel):
    model_config = ConfigDict(extra="forbid")
    code: Literal["INTERNAL_ERROR", "REQUEST_INVALID", "NOT_FOUND", "DEPENDENCY_UNAVAILABLE"]
    message: str
    request_id: UUID
    details: ErrorDetails
    retryable: bool


class ErrorEnvelope(BaseModel):
    model_config = ConfigDict(extra="forbid")
    error: ErrorPayload


def error_response(status: int, code: str, message: str, request_id: str) -> JSONResponse:
    return JSONResponse(
        status_code=status,
        content={
            "error": {
                "code": code,
                "message": message,
                "request_id": request_id,
                "details": {},
                "retryable": status in {429, 503},
            }
        },
    )


def create_app(settings: Settings | None = None) -> FastAPI:
    settings = settings or Settings()  # type: ignore[call-arg]

    @asynccontextmanager
    async def lifespan(app: FastAPI) -> AsyncIterator[None]:
        db = Database(settings)
        app.state.database = db
        try:
            yield
        finally:
            await db.close()

    local_docs = settings.environment in {"local", "test"}
    app = FastAPI(
        title="NEKI API",
        version="0.1.0",
        lifespan=lifespan,
        docs_url="/docs" if local_docs else None,
        redoc_url=None,
        openapi_url="/openapi.json" if local_docs else None,
    )

    @app.exception_handler(HTTPException)
    async def http_error(request: Request, exc: HTTPException) -> JSONResponse:
        return error_response(
            exc.status_code,
            "NOT_FOUND" if exc.status_code == 404 else "REQUEST_INVALID",
            "Resource not found." if exc.status_code == 404 else "Request not allowed.",
            request.state.request_id,
        )

    @app.exception_handler(RequestValidationError)
    async def validation_error(request: Request, exc: RequestValidationError) -> JSONResponse:
        return error_response(
            422, "REQUEST_INVALID", "Check the request fields.", request.state.request_id
        )

    @app.get("/health/live", response_model=Health, operation_id="platform_liveness")
    async def live() -> Health:
        return Health(status="ok")

    @app.get(
        "/health/ready",
        response_model=Health,
        operation_id="platform_readiness",
        responses={
            503: {
                "model": ErrorEnvelope,
                "description": "Database or migration revision unavailable",
            }
        },
    )
    async def ready(request: Request) -> Health | JSONResponse:
        if not await request.app.state.database.ready():
            return error_response(
                503, "DEPENDENCY_UNAVAILABLE", "Service is not ready.", request.state.request_id
            )
        return Health(status="ready")

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.allowed_origins,
        allow_credentials=True,
        allow_methods=["GET", "POST", "PATCH", "DELETE"],
        allow_headers=[
            "Authorization",
            "Content-Type",
            "X-Request-ID",
            "X-CSRF-Token",
            "Idempotency-Key",
        ],
        expose_headers=["X-Request-ID"],
    )
    app.add_middleware(RequestContext)
    return app
