from concurrent.futures import ThreadPoolExecutor
from uuid import UUID, uuid4

import psycopg
import pytest
from conftest import migrate
from fastapi.testclient import TestClient

from neki_api.config import Settings
from neki_api.main import create_app

pytestmark = pytest.mark.postgres


@pytest.fixture
def identity_client(database):
    migrate(database, "upgrade", "head")
    app = create_app(
        Settings(
            database_url=database,
            environment="test",
            sms_provider="test",
            auth_secret="synthetic-only-test-key-" * 4,
            allowed_origins=["https://testserver"],
        )
    )
    with TestClient(app, base_url="https://testserver") as client:
        yield client


def challenge(client, phone="+919000000001", kind="mobile"):
    device = str(uuid4())
    result = client.post(
        "/v1/auth/otp/request",
        json={
            "phone_e164": phone,
            "device_id": device,
            "client_kind": kind,
        },
        headers={"origin": "https://testserver"},
    )
    assert result.status_code == 200, result.text
    cid = result.json()["challenge_id"]
    assert "code" not in result.json()
    return {
        "challenge_id": cid,
        "device_id": device,
        "client_kind": kind,
        "code": client.app.state.identity.test_delivery[UUID(cid)],
    }


def login(client, phone="+919000000001", kind="mobile"):
    body = challenge(client, phone, kind)
    result = client.post("/v1/auth/otp/verify", json=body, headers={"origin": "https://testserver"})
    assert result.status_code == 200, result.text
    return result.json(), body["device_id"]


def bearer(session):
    return {"authorization": "Bearer " + session["access_token"]}


def sql(database, statement, params=()):
    with psycopg.connect(database.replace("postgresql+psycopg://", "postgresql://")) as db:
        return (
            db.execute(statement, params).fetchall()
            if "returning" in statement.lower()
            else db.execute(statement, params)
        )


def test_signup_profile_privacy_owner_and_mass_assignment(identity_client):
    client = identity_client
    first, _ = login(client)
    second, _ = login(client, "+919000000002")
    assert client.get("/v1/me").status_code == 401
    me = client.get("/v1/me", headers=bearer(first)).json()
    assert me["id"] == first["user_id"] and not me["profile_complete"]
    assert "phone_e164" not in me
    assert (
        client.patch(
            "/v1/me", headers=bearer(first), json={"expected_version": 1, "role": "super_admin"}
        ).status_code
        == 422
    )
    assert (
        client.patch(
            "/v1/me", headers=bearer(first), json={"expected_version": 1, "first_name": "Asha"}
        ).json()["version"]
        == 2
    )
    assert (
        client.patch(
            "/v1/me", headers=bearer(first), json={"expected_version": 1, "first_name": "Stale"}
        ).status_code
        == 409
    )
    assert client.get("/v1/me", headers=bearer(second)).json()["first_name"] is None
    private = client.get("/v1/me/privacy", headers=bearer(first)).json()
    assert private == {
        "profile_public": False,
        "contributions_public": False,
        "impact_sharing": False,
        "version": 1,
    }
    assert (
        client.patch(
            "/v1/me/privacy",
            headers=bearer(first),
            json={
                "profile_public": True,
                "contributions_public": False,
                "impact_sharing": False,
                "expected_version": 1,
            },
        ).status_code
        == 200
    )
    assert client.get("/v1/me/privacy", headers=bearer(second)).json() == private


def test_otp_attempts_commit_and_phone_lock_survives_new_device(identity_client):
    client = identity_client
    data = challenge(client)
    wrong = dict(data, code="000000" if data["code"] != "000000" else "999999")
    for _ in range(4):
        assert client.post("/v1/auth/otp/verify", json=wrong).status_code == 401
    fifth = client.post("/v1/auth/otp/verify", json=wrong)
    assert fifth.status_code == 429 and fifth.headers["retry-after"] == "900"
    assert client.post("/v1/auth/otp/verify", json=data).status_code == 429
    assert (
        client.post(
            "/v1/auth/otp/request",
            json={
                "phone_e164": "+919000000001",
                "device_id": str(uuid4()),
                "client_kind": "mobile",
            },
        ).status_code
        == 429
    )


def test_single_use_otp_concurrent_and_expiry(identity_client, database):
    client = identity_client
    data = challenge(client)
    with ThreadPoolExecutor(2) as pool:
        statuses = list(
            pool.map(lambda _: client.post("/v1/auth/otp/verify", json=data).status_code, range(2))
        )
    assert sorted(statuses) == [200, 401]
    expired = challenge(client, "+919000000002")
    sql(
        database,
        "UPDATE auth_challenges SET expires_at=now()-interval '1 second' WHERE id=%s",
        (expired["challenge_id"],),
    )
    assert client.post("/v1/auth/otp/verify", json=expired).json()["error"]["code"] == "OTP_EXPIRED"


def test_device_and_client_binding_do_not_consume_otp(identity_client):
    client = identity_client
    data = challenge(client)
    assert (
        client.post("/v1/auth/otp/verify", json=dict(data, device_id=str(uuid4()))).status_code
        == 401
    )
    assert (
        client.post(
            "/v1/auth/otp/verify",
            json=dict(data, client_kind="web"),
            headers={"origin": "https://testserver"},
        ).status_code
        == 401
    )
    assert client.post("/v1/auth/otp/verify", json=data).status_code == 200


def test_refresh_reuse_revokes_family_and_access_immediately(identity_client):
    client = identity_client
    session, device = login(client)
    body = {"client_kind": "mobile", "device_id": device, "refresh_token": session["refresh_token"]}
    wrong = client.post("/v1/auth/refresh", json=dict(body, device_id=str(uuid4())))
    assert wrong.status_code == 401
    rotated = client.post("/v1/auth/refresh", json=body)
    assert rotated.status_code == 200
    assert rotated.json()["refresh_token"] != session["refresh_token"]
    assert client.post("/v1/auth/refresh", json=body).json()["error"]["code"] == "REFRESH_REUSED"
    assert client.get("/v1/me", headers=bearer(rotated.json())).status_code == 401
    assert (
        client.post(
            "/v1/auth/refresh", json=dict(body, refresh_token=rotated.json()["refresh_token"])
        ).status_code
        == 401
    )


def test_concurrent_refresh_has_one_winner_and_revokes_on_replay(identity_client):
    client = identity_client
    session, device = login(client)
    body = {"client_kind": "mobile", "device_id": device, "refresh_token": session["refresh_token"]}
    with ThreadPoolExecutor(2) as pool:
        results = list(pool.map(lambda _: client.post("/v1/auth/refresh", json=body), range(2)))
    assert sorted(r.status_code for r in results) == [200, 401]
    assert (
        client.get(
            "/v1/me", headers=bearer(next(r.json() for r in results if r.status_code == 200))
        ).status_code
        == 401
    )


def test_logout_suspension_and_deleted_session_block_old_access(identity_client, database):
    client = identity_client
    first, _ = login(client)
    assert (
        client.post(
            "/v1/auth/logout", headers=bearer(first), json={"expected_version": 2}
        ).status_code
        == 409
    )
    assert (
        client.post(
            "/v1/auth/logout", headers=bearer(first), json={"expected_version": 1}
        ).status_code
        == 200
    )
    assert client.get("/v1/me", headers=bearer(first)).status_code == 401
    second, device = login(client, "+919000000002")
    sql(database, "UPDATE users SET status='SUSPENDED' WHERE id=%s", (second["user_id"],))
    assert client.get("/v1/me", headers=bearer(second)).status_code == 401
    assert (
        client.post(
            "/v1/auth/refresh",
            json={
                "client_kind": "mobile",
                "device_id": device,
                "refresh_token": second["refresh_token"],
            },
        ).status_code
        == 403
    )


def test_browser_cookie_transport_csrf_origin_and_rotation(identity_client):
    client = identity_client
    session, device = login(client, kind="web")
    assert "refresh_token" not in session and "refresh_expires_at" not in session
    cookie = next(c for c in client.cookies.jar if c.name == "__Host-neki-refresh")
    assert cookie.secure and cookie.has_nonstandard_attr("HttpOnly") and cookie.path == "/"
    csrf = client.cookies.get("__Host-neki-csrf")
    body = {"client_kind": "web", "device_id": device}
    assert (
        client.post(
            "/v1/auth/refresh", json=body, headers={"origin": "https://testserver"}
        ).status_code
        == 403
    )
    assert (
        client.post(
            "/v1/auth/refresh",
            json=body,
            headers={"origin": "https://evil.example", "x-csrf-token": csrf},
        ).status_code
        == 403
    )
    assert (
        client.post("/v1/auth/refresh", json=dict(body, refresh_token="x" * 48)).status_code == 422
    )
    assert (
        client.post(
            "/v1/auth/refresh",
            json={"client_kind": "mobile", "device_id": device, "refresh_token": cookie.value},
        ).status_code
        == 403
    )
    result = client.post(
        "/v1/auth/refresh",
        json=body,
        headers={"origin": "https://testserver", "x-csrf-token": csrf},
    )
    assert result.status_code == 200 and "refresh_token" not in result.json()
    assert client.cookies.get("__Host-neki-csrf") != csrf
    assert (
        client.post(
            "/v1/auth/logout", json={"expected_version": 1}, headers=bearer(result.json())
        ).status_code
        == 200
    )
    assert not list(client.cookies.jar)


def test_provider_disabled_fails_closed_without_otp_or_credentials(database):
    with TestClient(create_app(Settings(database_url=database, environment="test"))) as client:
        response = client.post(
            "/v1/auth/otp/request",
            json={
                "phone_e164": "+919000000001",
                "device_id": str(uuid4()),
                "client_kind": "mobile",
            },
        )
        assert response.status_code == 503
        assert "code_hash" not in response.text
