"""
Unit tests for message service.
Tests core business logic for message limits and validation.
"""

import pytest
from datetime import datetime, timedelta
from app.services.message_service import MessageValidationService
from app.models.message import Message


@pytest.mark.unit
class TestMessageLimits:
    """Test message limit calculations."""

    def test_athlete_daily_limit_not_exceeded(self, db_session, athlete1, athlete2):
        """Athlete with < 100 messages should not exceed daily limit."""
        # Create 50 messages
        for i in range(50):
            msg = Message(
                sender_id=athlete1.id,
                recipient_id=athlete2.id,
                content=f"Message {i}"
            )
            db_session.add(msg)
        db_session.commit()

        limits = MessageValidationService.get_message_limits(db_session, athlete1.id)
        
        assert limits["total_today"] == 50
        assert limits["daily_limit"] == 100
        assert limits["is_exceeded"] is False

    def test_athlete_daily_limit_exceeded(self, db_session, athlete1, athlete2):
        """Athlete with 100+ messages should exceed daily limit."""
        # Create 100 messages
        for i in range(100):
            msg = Message(
                sender_id=athlete1.id,
                recipient_id=athlete2.id,
                content=f"Message {i}"
            )
            db_session.add(msg)
        db_session.commit()

        limits = MessageValidationService.get_message_limits(db_session, athlete1.id)
        
        assert limits["total_today"] == 100
        assert limits["daily_limit"] == 100
        assert limits["is_exceeded"] is True

    def test_official_limit_not_exceeded(self, db_session, athlete1, official, exchange_accepted):
        """Athlete with < 5 messages to official should not exceed."""
        # Create 3 messages to official
        for i in range(3):
            msg = Message(
                sender_id=athlete1.id,
                recipient_id=official.id,
                content=f"Message {i}"
            )
            db_session.add(msg)
        db_session.commit()

        limits = MessageValidationService.get_message_limits(
            db_session, athlete1.id, official.id
        )
        
        assert limits["to_official"] == 3
        assert limits["official_limit"] == 5

    def test_official_has_no_limits(self, db_session, official, athlete1):
        """Officials should have no daily limits."""
        # Create 150 messages (exceeds athlete limit)
        for i in range(150):
            msg = Message(
                sender_id=official.id,
                recipient_id=athlete1.id,
                content=f"Message {i}"
            )
            db_session.add(msg)
        db_session.commit()

        limits = MessageValidationService.get_message_limits(db_session, official.id)
        
        assert limits["total_today"] == 150
        assert limits["daily_limit"] is None
        assert limits["is_exceeded"] is False


@pytest.mark.unit
class TestMessageValidation:
    """Test message sending validation."""

    def test_can_message_athlete_to_athlete(self, db_session, athlete1, athlete2):
        """Athletes should be able to message each other without exchange."""
        result = MessageValidationService.can_send_message(
            db_session, athlete1.id, athlete2.id
        )
        
        assert result["allowed"] is True
        assert result.get("reason") is None

    def test_cannot_message_without_exchange(self, db_session, athlete1, official):
        """Athlete cannot message official without exchange."""
        result = MessageValidationService.can_send_message(
            db_session, athlete1.id, official.id
        )
        
        assert result["allowed"] is False
        assert "exchange" in result["reason"].lower()

    def test_cannot_exceed_daily_limit(self, db_session, athlete1, athlete2):
        """Cannot send message when daily limit exceeded."""
        # Create 100 messages
        for i in range(100):
            msg = Message(
                sender_id=athlete1.id,
                recipient_id=athlete2.id,
                content=f"Message {i}"
            )
            db_session.add(msg)
        db_session.commit()

        result = MessageValidationService.can_send_message(
            db_session, athlete1.id, athlete2.id
        )
        
        assert result["allowed"] is False
        assert "limit" in result["reason"].lower()