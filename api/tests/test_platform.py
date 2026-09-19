from uuid import UUID, uuid4

import pytest
from fastapi.testclient import TestClient
from pydantic import ValidationError

from neki_api.config import Settings
from neki_api.main import create_app

URL = "postgresql+psycopg://synthetic:never-log-this@127.0.0.1:1/neki_test"


def settings(**overrides):
    return Settings(database_url=URL, **overrides)


@pytest.mark.parametrize(
    "patch",
    [
        {"database_url": "sqlite:///test.db"},
        {"database_url": "not-a-url-with-never-log-this"},
        {"environment": "production"},
        {"payments_enabled": True},
        {"allowed_origins": ["*"]},
        {"allowed_origins": ["https://example.org/path"]},
        {"allowed_origins": ["https://user:secret@example.org"]},
    ],
)
def test_invalid_settings_fail_without_echoing_secrets(patch):
    values = {"database_url": URL} | patch
    with pytest.raises(ValidationError) as error:
        Settings(**values)
    assert "never-log-this" not in str(error.value)


def test_test_provider_cannot_boot_in_staging():
    with pytest.raises(ValidationError, match="test SMS provider"):
        Settings(
            environment="staging",
            sms_provider="test",
            database_url="postgresql+psycopg://fixture:fixture@database.example/neki?sslmode=verify-full",
        )


def test_liveness_does_not_depend_on_database_and_request_id_is_bounded():
    with TestClient(create_app(settings())) as client:
        response = client.get("/health/live", headers={"X-Request-ID": "untrusted-value"})
        assert response.status_code == 200
        assert response.json() == {"status": "ok"}
        UUID(response.headers["x-request-id"])
        assert response.headers["cache-control"] == "no-store"
        known = str(uuid4())
        assert (
            client.get("/health/live", headers={"X-Request-ID": known}).headers["x-request-id"]
            == known
        )


def test_readiness_fails_closed_without_disclosing_driver_error():
    with TestClient(create_app(settings(database_timeout_seconds=0.2))) as client:
        response = client.get("/health/ready")
        assert response.status_code == 503
        error = response.json()["error"]
        assert error["code"] == "DEPENDENCY_UNAVAILABLE"
        assert error["request_id"] == response.headers["x-request-id"]
        assert error["retryable"] is True
        assert "never-log-this" not in response.text
        assert "127.0.0.1" not in response.text


def test_unimplemented_routes_are_not_placeholder_success():
    with TestClient(create_app(settings())) as client:
        response = client.get("/v1/not-implemented")
        assert response.status_code == 404
        assert response.json()["error"]["code"] == "NOT_FOUND"


def test_exception_and_validation_details_cannot_echo_private_input(caplog):
    app = create_app(settings())

    @app.get("/test/crash")
    async def crash():
        raise RuntimeError("never-log-this phone/private/provider")

    @app.get("/test/validate")
    async def validate(count: int):
        return {"count": count}

    with TestClient(app) as client:
        crash_response = client.get("/test/crash")
        assert crash_response.status_code == 500
        assert crash_response.json()["error"]["code"] == "INTERNAL_ERROR"
        invalid = client.get("/test/validate?count=never-log-this")
        assert invalid.status_code == 422
        assert invalid.json()["error"]["details"] == {}
    assert "never-log-this" not in crash_response.text + invalid.text + caplog.text


def test_cors_preflight_is_exact_and_has_request_context():
    with TestClient(create_app(settings(allowed_origins=["https://portal.example"]))) as client:
        allowed = client.options(
            "/health/live",
            headers={"Origin": "https://portal.example", "Access-Control-Request-Method": "GET"},
        )
        assert allowed.status_code == 200
        assert allowed.headers["access-control-allow-origin"] == "https://portal.example"
        assert "x-request-id" in allowed.headers
        denied = client.options(
            "/health/live",
            headers={
                "Origin": "https://portal.example.evil",
                "Access-Control-Request-Method": "GET",
            },
        )
        assert denied.status_code == 400
        assert "access-control-allow-origin" not in denied.headers


def test_runtime_schema_describes_implemented_routes_only():
    app = create_app(settings())
    schema = app.openapi()
    assert {"/health/live", "/health/ready", "/v1/me", "/v1/auth/refresh"} <= set(schema["paths"])
    assert "/v1/payments" not in schema["paths"]
    assert "ErrorEnvelope" in schema["components"]["schemas"]


def test_deployed_docs_are_disabled():
    app = create_app(
        Settings(
            environment="production",
            database_url="postgresql+psycopg://fixture:fixture@database.example/neki?sslmode=verify-full",
        )
    )
    with TestClient(app) as client:
        assert client.get("/openapi.json").status_code == 404
        assert client.get("/docs").status_code == 404
