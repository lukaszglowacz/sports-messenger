"""
Models package initialization.

Exports all database models for easy importing.
"""

from app.models.user import User, UserType
from app.models.contact_exchange import ContactExchange, ContactExchangeStatus
from app.models.message import Message

__all__ = [
    "User",
    "UserType",
    "ContactExchange",
    "ContactExchangeStatus",
    "Message",
]
