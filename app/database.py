"""
Database configuration and session management.
Sets up SQLAlchemy engine and session factory.
"""

import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from contextlib import contextmanager
import logging

from app.config import get_settings

# Load configuration
settings = get_settings()

# Configure logging for database operations
logger = logging.getLogger(__name__)

# Detect serverless environment (Vercel, etc.)
IS_SERVERLESS = bool(os.getenv("VERCEL")) or bool(os.getenv("AWS_LAMBDA_FUNCTION_NAME"))

# Determine database URL for serverless environments
database_url = settings.DATABASE_URL
if IS_SERVERLESS and database_url.startswith("sqlite:///"):
    # Vercel filesystem is read-only except /tmp
    database_url = database_url.replace("sqlite:///", "sqlite:////tmp/")
    logger.info(f"Serverless detected: using /tmp database at {database_url}")

# Create SQLAlchemy engine
# connect_args needed for SQLite to handle foreign keys properly
connect_args = {}
if "sqlite" in database_url:
    connect_args["check_same_thread"] = False

engine = create_engine(
    database_url,
    connect_args=connect_args,
    echo=settings.DEBUG,  # Log SQL queries in debug mode
    pool_pre_ping=True,   # Verify connections before using
)

# Create session factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

# Base class for all SQLAlchemy models
Base = declarative_base()


def get_db() -> Session:
    """
    FastAPI dependency that provides a database session.
    Automatically closes the session after the request is complete.
    Use this in your route functions.
    
    Yields:
        Session: SQLAlchemy database session
    """
    db = SessionLocal()
    try:
        yield db
    except Exception as e:
        logger.error(f"Database session error: {e}")
        db.rollback()
        raise
    finally:
        db.close()


@contextmanager
def get_db_context():
    """
    Context manager for database sessions.
    Useful for background tasks or scripts outside of request context.
    
    Usage:
        with get_db_context() as db:
            # use db session
    """
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


def create_tables():
    """
    Create all database tables defined in models.
    Called on application startup.
    """
    logger.info("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    logger.info("Database tables created successfully.")


def drop_tables():
    """
    Drop all database tables.
    Useful for testing or database resets.
    """
    logger.warning("Dropping all database tables...")
    Base.metadata.drop_all(bind=engine)
    logger.warning("All database tables dropped.")
