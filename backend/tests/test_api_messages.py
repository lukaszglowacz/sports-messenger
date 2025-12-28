"""
Integration tests for message API endpoints.
"""

import pytest
from app.models.message import Message


@pytest.mark.integration
class TestMessagesAPI:
    """Test message API endpoints."""

    def test_send_message_success(self, client, athlete1, athlete2):
        """Should successfully send message between athletes."""
        response = client.post("/api/messages", json={
            "sender_id": athlete1.id,
            "recipient_id": athlete2.id,
            "content": "Hello!"
        })
        
        assert response.status_code == 201
        data = response.json()
        assert data["content"] == "Hello!"
        assert data["sender_id"] == athlete1.id

    def test_send_message_without_exchange(self, client, athlete1, official):
        """Should fail when sending to official without exchange."""
        response = client.post("/api/messages", json={
            "sender_id": athlete1.id,
            "recipient_id": official.id,
            "content": "Hello!"
        })
        
        assert response.status_code == 400

    def test_send_message_exceeding_daily_limit(self, client, db_session, athlete1, athlete2):
        """Should return 429 when daily limit exceeded."""
        # Create 100 messages
        for i in range(100):
            msg = Message(
                sender_id=athlete1.id,
                recipient_id=athlete2.id,
                content=f"Message {i}"
            )
            db_session.add(msg)
        db_session.commit()

        response = client.post("/api/messages", json={
            "sender_id": athlete1.id,
            "recipient_id": athlete2.id,
            "content": "One too many"
        })
        
        assert response.status_code == 429

    def test_get_message_limits_athlete(self, client, athlete1):
        """Should return limits for athlete."""
        response = client.get(f"/api/messages/limits?user_id={athlete1.id}")
        
        assert response.status_code == 200
        data = response.json()
        assert data["daily_limit"] == 100
        assert data["is_exceeded"] is False