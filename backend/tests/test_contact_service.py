"""
Unit tests for contact service.
"""

import pytest
from app.services.contact_service import ContactService
from app.models.contact_exchange import ContactExchangeStatus


@pytest.mark.unit
class TestContactService:
    """Test contact service logic."""

    def test_get_contacts_for_athlete(self, db_session, athlete1, athlete2):
        """Should return contacts for athlete."""
        contacts = ContactService.get_contacts_for_user(db_session, athlete1.id)
        
        assert "contacts" in contacts
        assert "pending_requests" in contacts
        assert "potential_contacts" in contacts

    def test_create_exchange_request(self, db_session, athlete1, official):
        """Should create exchange request."""
        exchange = ContactService.create_exchange_request(
            db_session,
            from_user_id=athlete1.id,
            to_user_id=official.id
        )
        
        assert exchange.athlete_id == athlete1.id
        assert exchange.official_id == official.id
        assert exchange.status == ContactExchangeStatus.PENDING

    def test_accept_exchange(self, db_session, exchange_pending, official):
        """Should accept exchange request."""
        accepted = ContactService.accept_exchange(
            db_session,
            exchange_pending.id,
            official.id
        )
        
        assert accepted.status == ContactExchangeStatus.ACCEPTED

    def test_reject_exchange(self, db_session, exchange_pending, official):
        """Should reject exchange request."""
        rejected = ContactService.reject_exchange(
            db_session,
            exchange_pending.id,
            official.id
        )
        
        assert rejected.status == ContactExchangeStatus.REJECTED