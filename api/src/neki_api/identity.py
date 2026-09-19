"""Identity boundary. Credentials never enter profiles, events or request logs."""

import hashlib
import hmac
import secrets
from datetime import UTC, datetime, timedelta
from typing import Annotated, Any, Literal
from uuid import UUID, uuid4

import jwt
from fastapi import APIRouter, Depends, Request, Response
from pydantic import BaseModel, ConfigDict, Field, model_validator
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from neki_api.config import Settings
from neki_api.database import Database
from neki_api.errors import DomainError


class Input(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)


class OtpRequest(Input):
    phone_e164: str = Field(pattern=r"^\+[1-9][0-9]{7,14}$")
    device_id: UUID
    client_kind: Literal["mobile", "web"]


class OtpVerify(Input):
    challenge_id: UUID
    code: str = Field(pattern=r"^[0-9]{6}$", repr=False)
    device_id: UUID
    client_kind: Literal["mobile", "web"]


class Challenge(Input):
    challenge_id: UUID
    expires_at: datetime
    resend_after: datetime
    delivery_status: Literal["accepted"] = "accepted"
    code_length: Literal[6] = 6


class WebSession(Input):
    client_kind: Literal["web"] = "web"
    access_token: str
    token_type: Literal["Bearer"] = "Bearer"
    access_expires_at: datetime
    session_id: UUID
    user_id: UUID
    profile_complete: bool


class MobileSession(Input):
    client_kind: Literal["mobile"] = "mobile"
    access_token: str
    token_type: Literal["Bearer"] = "Bearer"
    access_expires_at: datetime
    session_id: UUID
    user_id: UUID
    profile_complete: bool
    refresh_token: str
    refresh_expires_at: datetime


SessionResult = Annotated[WebSession | MobileSession, Field(discriminator="client_kind")]


class MobileRefresh(Input):
    client_kind: Literal["mobile"]
    device_id: UUID
    refresh_token: str = Field(min_length=32, max_length=4096, repr=False)


class WebRefresh(Input):
    client_kind: Literal["web"]
    device_id: UUID


Refresh = Annotated[MobileRefresh | WebRefresh, Field(discriminator="client_kind")]


class VersionCommand(Input):
    expected_version: int = Field(ge=1)


class Revocation(Input):
    session_id: UUID
    revoked: Literal[True] = True
    version: int


class Profile(Input):
    id: UUID
    first_name: str | None
    last_name: str | None
    avatar_media_id: UUID | None = None
    impact_statement: str
    locale: Literal["en-IN"] = "en-IN"
    profile_complete: bool
    account_status: Literal["ACTIVE", "SUSPENDED", "DELETION_PENDING"]
    version: int


class ProfileUpdate(VersionCommand):
    first_name: str | None = Field(default=None, min_length=1, max_length=80)
    last_name: str | None = Field(default=None, min_length=1, max_length=80)
    impact_statement: str | None = Field(default=None, max_length=200)

    @model_validator(mode="after")
    def valid_patch(self) -> "ProfileUpdate":
        if self.model_fields_set == {"expected_version"}:
            raise ValueError("At least one profile field is required")
        for key in ("first_name", "impact_statement"):
            if key in self.model_fields_set and getattr(self, key) is None:
                raise ValueError("Field cannot be null")
        return self


class Privacy(Input):
    profile_public: bool
    contributions_public: bool
    impact_sharing: bool
    version: int


class PrivacyUpdate(VersionCommand):
    profile_public: bool
    contributions_public: bool
    impact_sharing: bool


class Principal(BaseModel):
    user_id: UUID
    session_id: UUID
    device_id: UUID
    client_kind: str


def profile(row: Any) -> Profile:
    return Profile(
        id=row["id"],
        first_name=row["first_name"],
        last_name=row["last_name"],
        impact_statement=row["impact_statement"],
        account_status=row["status"],
        profile_complete=bool(row["first_name"]),
        version=row["version"],
    )


class Identity:
    def __init__(self, db: Database, settings: Settings) -> None:
        self.db, self.settings = db, settings
        # Explicitly local/test only; never exposed by HTTP or logging.
        self.test_delivery: dict[UUID, str] = {}

    def digest(self, purpose: str, value: str) -> str:
        if not self.settings.auth_secret:
            raise DomainError("DEPENDENCY_UNAVAILABLE", 503)
        return hmac.new(
            self.settings.auth_secret.get_secret_value().encode(),
            f"{purpose}:{value}".encode(),
            hashlib.sha256,
        ).hexdigest()

    def browser_origin(self, request: Request) -> None:
        if request.headers.get("origin") not in self.settings.allowed_origins:
            raise DomainError("ACTION_FORBIDDEN", 403)
        if request.url.scheme != "https":
            raise DomainError("ACTION_FORBIDDEN", 403)

    async def request_otp(self, data: OtpRequest, request: Request) -> Challenge:
        if self.settings.sms_provider != "test" or self.settings.environment not in {
            "local",
            "test",
        }:
            # MSG91 onboarding and durable delivery adapter are not implemented yet.
            raise DomainError("DEPENDENCY_UNAVAILABLE", 503)
        if data.client_kind == "web":
            self.browser_origin(request)
        now = datetime.now(UTC)
        phone_scope = self.digest("phone", data.phone_e164)
        scopes = {
            phone_scope: (5, 60),
            self.digest("device", str(data.device_id)): (5, 60),
            self.digest("ip", request.client.host if request.client else "unknown"): (30, 0),
        }
        challenge_id, code = uuid4(), f"{secrets.randbelow(1_000_000):06d}"
        async with self.db.transaction() as db:
            # Sorted lock order serializes concurrent abuse checks, including phone verification.
            for scope in sorted(scopes):
                await db.execute(
                    text("SELECT pg_advisory_xact_lock(hashtextextended(:s,0))"), {"s": scope}
                )
                await db.execute(
                    text("INSERT INTO auth_limits(scope) VALUES(:s) ON CONFLICT DO NOTHING"),
                    {"s": scope},
                )
                limit = (
                    (
                        await db.execute(
                            text("SELECT * FROM auth_limits WHERE scope=:s"), {"s": scope}
                        )
                    )
                    .mappings()
                    .one()
                )
                count = limit["requests"] if limit["window_start"] > now - timedelta(hours=1) else 0
                if (
                    limit["locked_until"] > now
                    or limit["next_allowed"] > now
                    or count >= scopes[scope][0]
                ):
                    raise DomainError("OTP_RATE_LIMITED", 429, 60)
            for scope, (_, delay) in scopes.items():
                await db.execute(
                    text("""UPDATE auth_limits SET
                  requests=CASE WHEN window_start <= :now - interval '1 hour'
                    THEN 1 ELSE requests+1 END,
                  window_start=CASE WHEN window_start <= :now - interval '1 hour'
                    THEN :now ELSE window_start END,
                  next_allowed=:next WHERE scope=:s"""),
                    {"s": scope, "now": now, "next": now + timedelta(seconds=delay)},
                )
            await db.execute(
                text(
                    "UPDATE auth_challenges SET consumed_at=:now "
                    "WHERE phone_scope=:p AND consumed_at IS NULL"
                ),
                {"now": now, "p": phone_scope},
            )
            await db.execute(
                text("""INSERT INTO auth_challenges
              (id,phone_e164,phone_scope,device_id,client_kind,code_hash,expires_at)
              VALUES(:id,:phone,:scope,:device,:kind,:hash,:expires)"""),
                {
                    "id": challenge_id,
                    "phone": data.phone_e164,
                    "scope": phone_scope,
                    "device": data.device_id,
                    "kind": data.client_kind,
                    "hash": self.digest("otp", f"{challenge_id}:{code}"),
                    "expires": now + timedelta(minutes=5),
                },
            )
        self.test_delivery[challenge_id] = code
        return Challenge(
            challenge_id=challenge_id,
            expires_at=now + timedelta(minutes=5),
            resend_after=now + timedelta(seconds=60),
        )

    async def issue(
        self, db: AsyncSession, session: Any, user: Any, response: Response
    ) -> SessionResult:
        now, refresh = datetime.now(UTC), secrets.token_urlsafe(48)
        await db.execute(
            text("INSERT INTO refresh_tokens(token_hash,session_id) VALUES(:hash,:sid)"),
            {"hash": self.digest("refresh", refresh), "sid": session["id"]},
        )
        expires = now + timedelta(minutes=15)
        access = jwt.encode(
            {
                "sub": str(user["id"]),
                "sid": str(session["id"]),
                "iat": now,
                "exp": expires,
                "iss": "neki-api",
                "aud": "neki-client",
            },
            self.digest("jwt", "signing"),
            algorithm="HS256",
        )
        common = dict(
            access_token=access,
            access_expires_at=expires,
            session_id=session["id"],
            user_id=user["id"],
            profile_complete=bool(user["first_name"]),
        )
        if session["client_kind"] == "mobile":
            return MobileSession(
                **common, refresh_token=refresh, refresh_expires_at=session["expires_at"]
            )
        csrf = self.digest("csrf", f"{session['id']}:{session['device_id']}:{refresh}")
        age = max(0, int((session["expires_at"] - now).total_seconds()))
        response.set_cookie(
            "__Host-neki-refresh",
            refresh,
            max_age=age,
            secure=True,
            httponly=True,
            samesite="strict",
            path="/",
        )
        response.set_cookie(
            "__Host-neki-csrf",
            csrf,
            max_age=age,
            secure=True,
            httponly=False,
            samesite="strict",
            path="/",
        )
        return WebSession(**common)

    async def verify(self, data: OtpVerify, request: Request, response: Response) -> SessionResult:
        if data.client_kind == "web":
            self.browser_origin(request)
        failure: DomainError | None = None
        async with self.db.transaction() as db:
            found = (
                await db.execute(
                    text("SELECT phone_scope FROM auth_challenges WHERE id=:id"),
                    {"id": data.challenge_id},
                )
            ).scalar_one_or_none()
            if found is None:
                raise DomainError("OTP_INVALID", 401)
            await db.execute(
                text("SELECT pg_advisory_xact_lock(hashtextextended(:s,0))"), {"s": found}
            )
            row = (
                (
                    await db.execute(
                        text("SELECT * FROM auth_challenges WHERE id=:id FOR UPDATE"),
                        {"id": data.challenge_id},
                    )
                )
                .mappings()
                .one()
            )
            now = datetime.now(UTC)
            locked = (
                await db.execute(
                    text("SELECT locked_until > :now FROM auth_limits WHERE scope=:p"),
                    {"now": now, "p": found},
                )
            ).scalar_one()
            if locked or row["attempts"] >= 5:
                raise DomainError("OTP_LOCKED", 429, 900)
            if (
                row["consumed_at"]
                or row["device_id"] != data.device_id
                or row["client_kind"] != data.client_kind
            ):
                raise DomainError("OTP_INVALID", 401)
            if row["expires_at"] <= now:
                raise DomainError("OTP_EXPIRED", 401)
            if not hmac.compare_digest(
                row["code_hash"], self.digest("otp", f"{data.challenge_id}:{data.code}")
            ):
                await db.execute(
                    text("UPDATE auth_challenges SET attempts=attempts+1 WHERE id=:id"),
                    {"id": data.challenge_id},
                )
                if row["attempts"] == 4:
                    await db.execute(
                        text("UPDATE auth_limits SET locked_until=:until WHERE scope=:p"),
                        {"p": found, "until": now + timedelta(minutes=15)},
                    )
                # Commit failed-attempt counters before returning the public error.
                failure = (
                    DomainError("OTP_LOCKED", 429, 900)
                    if row["attempts"] == 4
                    else DomainError("OTP_INVALID", 401)
                )
            else:
                await db.execute(
                    text(
                        "INSERT INTO users(id,phone_e164) VALUES(:id,:phone) "
                        "ON CONFLICT(phone_e164) DO NOTHING"
                    ),
                    {"id": uuid4(), "phone": row["phone_e164"]},
                )
                user = (
                    (
                        await db.execute(
                            text("SELECT * FROM users WHERE phone_e164=:phone FOR UPDATE"),
                            {"phone": row["phone_e164"]},
                        )
                    )
                    .mappings()
                    .one()
                )
                if user["status"] != "ACTIVE":
                    raise DomainError("ACTION_FORBIDDEN", 403)
                await db.execute(
                    text(
                        "INSERT INTO user_roles(user_id,role) VALUES(:id,'contributor') "
                        "ON CONFLICT DO NOTHING"
                    ),
                    {"id": user["id"]},
                )
                await db.execute(
                    text(
                        "INSERT INTO privacy_preferences(user_id) VALUES(:id) "
                        "ON CONFLICT DO NOTHING"
                    ),
                    {"id": user["id"]},
                )
                await db.execute(
                    text("UPDATE auth_challenges SET consumed_at=:now WHERE id=:id"),
                    {"now": now, "id": data.challenge_id},
                )
                session = (
                    (
                        await db.execute(
                            text("""INSERT INTO auth_sessions
                  (id,user_id,device_id,client_kind,expires_at)
                  VALUES(:id,:uid,:device,:kind,:expires) RETURNING *"""),
                            {
                                "id": uuid4(),
                                "uid": user["id"],
                                "device": data.device_id,
                                "kind": data.client_kind,
                                "expires": now + timedelta(days=30),
                            },
                        )
                    )
                    .mappings()
                    .one()
                )
                result = await self.issue(db, session, user, response)
        if failure:
            raise failure
        self.test_delivery.pop(data.challenge_id, None)
        return result

    async def refresh(self, data: Refresh, request: Request, response: Response) -> SessionResult:
        cookie = request.cookies.get("__Host-neki-refresh")
        if data.client_kind == "web":
            self.browser_origin(request)
            token = cookie or ""
        else:
            if cookie or request.cookies.get("__Host-neki-csrf"):
                raise DomainError("ACTION_FORBIDDEN", 403)
            token = data.refresh_token
        token_hash = self.digest("refresh", token)
        reused = False
        async with self.db.transaction() as db:
            sid = (
                await db.execute(
                    text("SELECT session_id FROM refresh_tokens WHERE token_hash=:hash"),
                    {"hash": token_hash},
                )
            ).scalar_one_or_none()
            if sid is None:
                raise DomainError("REFRESH_INVALID", 401)
            session = (
                (
                    await db.execute(
                        text("SELECT * FROM auth_sessions WHERE id=:sid FOR UPDATE"), {"sid": sid}
                    )
                )
                .mappings()
                .one()
            )
            if session["client_kind"] != data.client_kind or session["device_id"] != data.device_id:
                raise DomainError("REFRESH_INVALID", 401)
            if data.client_kind == "web":
                expected = self.digest("csrf", f"{sid}:{data.device_id}:{token}")
                if not hmac.compare_digest(
                    request.headers.get("x-csrf-token", ""), expected
                ) or not hmac.compare_digest(request.cookies.get("__Host-neki-csrf", ""), expected):
                    raise DomainError("ACTION_FORBIDDEN", 403)
            if session["revoked_at"] or session["expires_at"] <= datetime.now(UTC):
                raise DomainError("REFRESH_INVALID", 401)
            # Read after the family lock; a concurrent rotation must observe the new consumption.
            consumed = (
                await db.execute(
                    text("SELECT consumed_at FROM refresh_tokens WHERE token_hash=:hash"),
                    {"hash": token_hash},
                )
            ).scalar_one()
            if consumed:
                await db.execute(
                    text(
                        "UPDATE auth_sessions SET revoked_at=now(),version=version+1 WHERE id=:sid"
                    ),
                    {"sid": sid},
                )
                reused = True
            else:
                user = (
                    (
                        await db.execute(
                            text("SELECT * FROM users WHERE id=:uid FOR SHARE"),
                            {"uid": session["user_id"]},
                        )
                    )
                    .mappings()
                    .one()
                )
                if user["status"] != "ACTIVE":
                    raise DomainError("ACTION_FORBIDDEN", 403)
                await db.execute(
                    text("UPDATE refresh_tokens SET consumed_at=now() WHERE token_hash=:hash"),
                    {"hash": token_hash},
                )
                result = await self.issue(db, session, user, response)
        if reused:
            raise DomainError("REFRESH_REUSED", 401)
        return result

    async def principal(self, request: Request) -> Principal:
        raw = request.headers.get("authorization", "")
        if not raw.startswith("Bearer "):
            raise DomainError("AUTH_REQUIRED", 401)
        try:
            claims = jwt.decode(
                raw[7:],
                self.digest("jwt", "signing"),
                algorithms=["HS256"],
                issuer="neki-api",
                audience="neki-client",
                options={"require": ["sub", "sid", "exp", "iat", "iss", "aud"]},
            )
            uid, sid = UUID(claims["sub"]), UUID(claims["sid"])
        except (jwt.InvalidTokenError, ValueError, TypeError, KeyError):
            raise DomainError("SESSION_EXPIRED", 401) from None
        async with self.db.transaction() as db:
            row = (
                (
                    await db.execute(
                        text("""SELECT s.* FROM auth_sessions s JOIN users u ON u.id=s.user_id
              WHERE s.id=:sid AND s.user_id=:uid AND s.revoked_at IS NULL
              AND s.expires_at > now() AND u.status='ACTIVE'"""),
                        {"sid": sid, "uid": uid},
                    )
                )
                .mappings()
                .one_or_none()
            )
            if row is None:
                raise DomainError("SESSION_EXPIRED", 401)
            return Principal(
                user_id=uid,
                session_id=sid,
                device_id=row["device_id"],
                client_kind=row["client_kind"],
            )


async def current_principal(request: Request) -> Principal:
    identity: Identity = request.app.state.identity
    return await identity.principal(request)


Current = Annotated[Principal, Depends(current_principal)]
router = APIRouter(prefix="/v1", tags=["identity"])


@router.post("/auth/otp/request", response_model=Challenge, operation_id="request_otp")
async def request_otp(data: OtpRequest, request: Request) -> Challenge:
    identity: Identity = request.app.state.identity
    return await identity.request_otp(data, request)


@router.post("/auth/otp/verify", response_model=SessionResult, operation_id="verify_otp")
async def verify_otp(data: OtpVerify, request: Request, response: Response) -> SessionResult:
    identity: Identity = request.app.state.identity
    return await identity.verify(data, request, response)


@router.post("/auth/refresh", response_model=SessionResult, operation_id="refresh_session")
async def refresh_session(data: Refresh, request: Request, response: Response) -> SessionResult:
    identity: Identity = request.app.state.identity
    return await identity.refresh(data, request, response)


@router.get("/me", response_model=Profile, operation_id="get_current_user")
async def get_me(request: Request, principal: Current) -> Profile:
    async with request.app.state.database.transaction() as db:
        row = (
            (await db.execute(text("SELECT * FROM users WHERE id=:id"), {"id": principal.user_id}))
            .mappings()
            .one()
        )
        return profile(row)


@router.patch("/me", response_model=Profile, operation_id="update_profile")
async def patch_me(data: ProfileUpdate, request: Request, principal: Current) -> Profile:
    changes = data.model_dump(exclude_unset=True, exclude={"expected_version"})
    # Names come only from the strict schema, never from unvalidated request keys.
    assignments = ",".join(f"{key}=:{key}" for key in changes)
    async with request.app.state.database.transaction() as db:
        row = (
            (
                await db.execute(
                    text(
                        f"UPDATE users SET {assignments},version=version+1 "
                        "WHERE id=:id AND version=:version AND status='ACTIVE' RETURNING *"
                    ),
                    {**changes, "id": principal.user_id, "version": data.expected_version},
                )
            )
            .mappings()
            .one_or_none()
        )
        if row is None:
            raise DomainError("VERSION_CONFLICT", 409)
        return profile(row)


@router.post("/auth/logout", response_model=Revocation, operation_id="logout_session")
async def logout(
    data: VersionCommand, request: Request, response: Response, principal: Current
) -> Revocation:
    async with request.app.state.database.transaction() as db:
        version = (
            await db.execute(
                text(
                    "UPDATE auth_sessions SET revoked_at=now(),version=version+1 "
                    "WHERE id=:id AND version=:version RETURNING version"
                ),
                {"id": principal.session_id, "version": data.expected_version},
            )
        ).scalar_one_or_none()
        if version is None:
            raise DomainError("VERSION_CONFLICT", 409)
    for name in ("__Host-neki-refresh", "__Host-neki-csrf"):
        response.delete_cookie(
            name, path="/", secure=True, httponly=name.endswith("refresh"), samesite="strict"
        )
    return Revocation(session_id=principal.session_id, version=version)


@router.get("/me/privacy", response_model=Privacy, operation_id="get_privacy_preferences")
async def get_privacy(request: Request, principal: Current) -> Privacy:
    async with request.app.state.database.transaction() as db:
        row = (
            (
                await db.execute(
                    text(
                        "SELECT profile_public,contributions_public,impact_sharing,version "
                        "FROM privacy_preferences WHERE user_id=:id"
                    ),
                    {"id": principal.user_id},
                )
            )
            .mappings()
            .one()
        )
        return Privacy(**row)


@router.patch("/me/privacy", response_model=Privacy, operation_id="set_privacy_preferences")
async def patch_privacy(data: PrivacyUpdate, request: Request, principal: Current) -> Privacy:
    async with request.app.state.database.transaction() as db:
        row = (
            (
                await db.execute(
                    text("""UPDATE privacy_preferences SET profile_public=:profile_public,
          contributions_public=:contributions_public,impact_sharing=:impact_sharing,version=version+1
          WHERE user_id=:id AND version=:expected_version
          RETURNING profile_public,contributions_public,impact_sharing,version"""),
                    {**data.model_dump(), "id": principal.user_id},
                )
            )
            .mappings()
            .one_or_none()
        )
        if row is None:
            raise DomainError("VERSION_CONFLICT", 409)
        return Privacy(**row)
