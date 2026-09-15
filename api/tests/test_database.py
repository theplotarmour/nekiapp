import asyncio
from uuid import uuid4

import psycopg
import pytest
from conftest import migrate
from fastapi.testclient import TestClient
from sqlalchemy import text

from neki_api.config import Settings
from neki_api.database import Database
from neki_api.main import create_app

pytestmark = pytest.mark.postgres


def dsn(url):
    return url.replace("postgresql+psycopg://", "postgresql://")


def test_empty_database_is_not_ready_then_migration_makes_it_ready(database):
    with TestClient(create_app(Settings(database_url=database, environment="test"))) as client:
        assert client.get("/health/ready").status_code == 503
        migrate(database, "upgrade", "head")
        assert client.get("/health/ready").json() == {"status": "ready"}
        with psycopg.connect(dsn(database)) as conn:
            conn.execute("update alembic_version set version_num='unknown_revision'")
        assert client.get("/health/ready").status_code == 503


def test_migration_downgrade_and_reapply(database):
    migrate(database, "upgrade", "head")
    migrate(database, "downgrade", "base")
    with psycopg.connect(dsn(database)) as conn:
        assert conn.execute("select to_regclass('domain_events')").fetchone()[0] is None
    migrate(database, "upgrade", "head")
    with psycopg.connect(dsn(database)) as conn:
        assert (
            conn.execute("select version_num from alembic_version").fetchone()[0] == "0001_platform"
        )


def test_session_context_rolls_back_failed_work_and_commits_success(database):
    migrate(database, "upgrade", "head")

    async def scenario():
        db = Database(Settings(database_url=database))
        try:
            with pytest.raises(RuntimeError):
                async with db.transaction() as session:
                    await session.execute(
                        text("insert into event_streams values ('test',:id,0)"), {"id": uuid4()}
                    )
                    raise RuntimeError("injected business failure")
            async with db.transaction() as session:
                assert (
                    await session.execute(text("select count(*) from event_streams"))
                ).scalar_one() == 0
                await session.execute(
                    text("insert into event_streams values ('test',:id,0)"), {"id": uuid4()}
                )
            async with db.transaction() as session:
                assert (
                    await session.execute(text("select count(*) from event_streams"))
                ).scalar_one() == 1
        finally:
            await db.close()

    asyncio.run(scenario())


def test_event_identity_fk_sequence_and_immutability_constraints(database):
    migrate(database, "upgrade", "head")
    aggregate, event = uuid4(), uuid4()
    with psycopg.connect(dsn(database)) as conn:
        conn.execute("insert into event_streams values ('test',%s,1)", (aggregate,))
        conn.execute(
            """insert into domain_events values
            (%s,'test',%s,1,1,'Test.v1',1,'{}','[]',%s,%s,%s,now())""",
            (event, aggregate, uuid4(), uuid4(), uuid4()),
        )
    with pytest.raises(psycopg.errors.CheckViolation):
        with psycopg.connect(dsn(database)) as conn:
            conn.execute("update domain_events set payload='{}' where id=%s", (event,))
    with pytest.raises(psycopg.errors.ForeignKeyViolation):
        with psycopg.connect(dsn(database)) as conn:
            conn.execute(
                "insert into event_handler_receipts(event_id,handler_name,handler_version) "
                "values (%s,'test',1)",
                (uuid4(),),
            )
    with pytest.raises(psycopg.errors.UniqueViolation):
        with psycopg.connect(dsn(database)) as conn:
            conn.execute(
                """insert into domain_events values
                (%s,'test',%s,1,1,'Test.v1',1,'{}','[]',%s,%s,%s,now())""",
                (uuid4(), aggregate, uuid4(), uuid4(), uuid4()),
            )
