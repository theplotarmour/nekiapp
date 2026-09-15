import asyncio
import os
import subprocess
import sys
from pathlib import Path
from uuid import uuid4

import psycopg
import pytest
from psycopg import sql

if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools/spikes"))
from postgres_runtime import PostgresRuntime  # noqa: E402


@pytest.fixture(scope="session")
def postgres():
    binary = os.environ.get("NEKI_TEST_PG_BIN")
    if not binary:
        pytest.skip("Set NEKI_TEST_PG_BIN to run isolated PostgreSQL integration tests")
    runtime = PostgresRuntime(binary)
    try:
        runtime.start()
        yield runtime
    finally:
        runtime.close()


@pytest.fixture
def database(postgres):
    name = "neki_test_" + uuid4().hex
    with psycopg.connect(postgres.dsn, autocommit=True) as conn:
        conn.execute(sql.SQL("create database {}").format(sql.Identifier(name)))
    url = f"postgresql+psycopg://{postgres.user}@127.0.0.1:{postgres.port}/{name}"
    try:
        yield url
    finally:
        with psycopg.connect(postgres.dsn, autocommit=True) as conn:
            conn.execute(sql.SQL("drop database {}").format(sql.Identifier(name)))


def migrate(url, *args):
    env = dict(os.environ, NEKI_DATABASE_URL=url, NEKI_ENVIRONMENT="test")
    result = subprocess.run(
        [sys.executable, "-m", "alembic", *args],
        cwd=ROOT / "api",
        env=env,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stderr
