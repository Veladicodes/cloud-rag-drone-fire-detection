"""SQLAlchemy engine / session setup.

LOCAL STAND-IN FOR: Azure SQL Database.
The models (see ``database/models.py``) use portable column types only, so the
same schema runs unmodified against Azure SQL once ``DATABASE_URL`` points there.
"""
from __future__ import annotations

from collections.abc import Iterator

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from backend.core.config import get_settings

settings = get_settings()

_url = settings.database_url
_connect_args = {"check_same_thread": False} if _url.startswith("sqlite") else {}

engine = create_engine(_url, connect_args=_connect_args, future=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False, future=True)


class Base(DeclarativeBase):
    """Declarative base shared by every ORM model."""


def init_db() -> None:
    """Create tables if they do not exist.

    Alembic migrations live in ``database/migrations/`` for real deployments;
    for the local prototype ``create_all`` is enough and keeps the demo one step.
    """
    import database.models  # noqa: F401  (register mappers)

    from backend.core.config import get_settings
    if get_settings().recreate_db:
        Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)


def get_db() -> Iterator[Session]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
