"""
Database Connection & Session Management Module.

Provides SQLAlchemy engine, session maker, Base declarative class,
and standard FastAPI dependency generator for database sessions.
"""

from typing import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker, Session
from app.core.config import settings

# Configure SQLite-specific args (check_same_thread=False) if using SQLite
connect_args = {"check_same_thread": False} if settings.DATABASE_URL.startswith("sqlite") else {}

engine = create_engine(
    settings.DATABASE_URL,
    connect_args=connect_args,
    echo=settings.DB_ECHO,
    pool_pre_ping=True,
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

Base = declarative_base()


def get_db() -> Generator[Session, None, None]:
    """
    FastAPI dependency yielding a thread-safe database session.
    Automatically commits or closes the session on exit.
    """
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()

