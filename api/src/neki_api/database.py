import asyncio
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from neki_api.config import Settings

SCHEMA_REVISION = "0002_identity"


class Database:
    def __init__(self, settings: Settings) -> None:
        self.timeout = settings.database_timeout_seconds
        self.engine = create_async_engine(
            settings.database_url.get_secret_value(),
            pool_size=settings.pool_size,
            max_overflow=0,
            pool_timeout=self.timeout,
            pool_pre_ping=True,
            hide_parameters=True,
            connect_args={
                "connect_timeout": max(1, int(self.timeout)),
                "options": f"-c statement_timeout={int(self.timeout * 1000)} -c timezone=UTC",
            },
        )
        self.sessions = async_sessionmaker(self.engine, expire_on_commit=False)

    @asynccontextmanager
    async def transaction(self) -> AsyncIterator[AsyncSession]:
        async with self.sessions.begin() as session:
            yield session

    async def ready(self) -> bool:
        try:
            async with asyncio.timeout(self.timeout):
                async with self.engine.connect() as conn:
                    revisions = (
                        (await conn.execute(text("select version_num from alembic_version")))
                        .scalars()
                        .all()
                    )
                    return revisions == [SCHEMA_REVISION]
        except Exception:
            # Connection strings, driver errors and SQL parameters never enter the response.
            return False

    async def close(self) -> None:
        await self.engine.dispose()
