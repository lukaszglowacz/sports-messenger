"""
Database configuration and session management.

This module sets up SQLAlchemy engine, session maker, and base model class.
Uses SQLite for simplicity in this demo application.
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# SQLite database URL
# For production, this should be configurable via environment variable
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./data/messenger.db")

# Create SQLAlchemy engine
# check_same_thread=False is needed for SQLite to work with FastAPI
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {}
)

# Create session maker
# Each request will get its own database session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for all database models
Base = declarative_base()


def get_db():
    """
    Dependency function to get database session.
    
    This function is used as a FastAPI dependency to provide
    database sessions to route handlers. It ensures proper
    cleanup after each request.
    
    Yields:
        Session: SQLAlchemy database session
        
    Example:
        @app.get("/users")
        def get_users(db: Session = Depends(get_db)):
            return db.query(User).all()
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """
    Initialize database tables.
    
    Creates all tables defined in models if they don't exist.
    This is called on application startup.
    """
    from app.models import user, message, contact_exchange
    Base.metadata.create_all(bind=engine)
