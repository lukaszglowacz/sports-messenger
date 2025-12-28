"""
Pytest configuration and fixtures for backend tests.
"""

import sys
from pathlib import Path

# Add parent directory to Python path
current_dir = Path(__file__).parent
parent_dir = current_dir.parent
sys.path.insert(0, str(parent_dir))

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.database import Base, get_db
from app.main import app
from app.models.user import User, UserType
from app.models.contact_exchange import ContactExchange, ContactExchangeStatus
from app.models.message import Message


# Test database configuration
SQLALCHEMY_TEST_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def db_session():
    """Create a fresh database for each test."""
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db_session):
    """Create a test client with dependency override."""
    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


@pytest.fixture
def athlete1(db_session):
    """Create test athlete 1."""
    user = User(
        id=1,
        name="Test Athlete 1",
        email="athlete1@test.com",
        type=UserType.ATHLETE
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


@pytest.fixture
def athlete2(db_session):
    """Create test athlete 2."""
    user = User(
        id=2,
        name="Test Athlete 2",
        email="athlete2@test.com",
        type=UserType.ATHLETE
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


@pytest.fixture
def official(db_session):
    """Create test official."""
    user = User(
        id=3,
        name="Test Official",
        email="official@test.com",
        type=UserType.OFFICIAL
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


@pytest.fixture
def exchange_accepted(db_session, athlete1, official):
    """Create accepted contact exchange between athlete1 and official."""
    exchange = ContactExchange(
        athlete_id=athlete1.id,
        official_id=official.id,
        initiated_by=athlete1.id,
        status=ContactExchangeStatus.ACCEPTED
    )
    db_session.add(exchange)
    db_session.commit()
    db_session.refresh(exchange)
    return exchange


@pytest.fixture
def exchange_pending(db_session, athlete2, official):
    """Create pending contact exchange between athlete2 and official."""
    exchange = ContactExchange(
        athlete_id=athlete2.id,
        official_id=official.id,
        initiated_by=athlete2.id,
        status=ContactExchangeStatus.PENDING
    )
    db_session.add(exchange)
    db_session.commit()
    db_session.refresh(exchange)
    return exchange


@pytest.fixture
def sample_messages(db_session, athlete1, athlete2):
    """Create sample messages between athletes."""
    messages = [
        Message(sender_id=athlete1.id, recipient_id=athlete2.id, content="Hello!"),
        Message(sender_id=athlete2.id, recipient_id=athlete1.id, content="Hi there!"),
        Message(sender_id=athlete1.id, recipient_id=athlete2.id, content="How are you?"),
    ]
    for msg in messages:
        db_session.add(msg)
    db_session.commit()
    return messages