"""
Message model.

Represents text messages exchanged between users.
"""

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean, Index
from sqlalchemy.orm import relationship
from datetime import datetime

from app.database import Base


class Message(Base):
    """
    Message model for storing chat messages.
    
    Messages can only contain text and emojis (validated at API level).
    No file attachments or images are supported.
    
    Attributes:
        id (int): Primary key
        sender_id (int): Foreign key to User who sent the message
        recipient_id (int): Foreign key to User who receives the message
        content (str): Message text (max 1000 characters)
        created_at (datetime): When message was sent
        read (bool): Whether recipient has read the message
        
    Relationships:
        sender: User who sent this message
        recipient: User who received this message
        
    Indexes:
        - sender_id, recipient_id, created_at: For efficient conversation queries
        - created_at: For date-based queries (daily limits)
    """
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    sender_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    recipient_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    content = Column(String(1000), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    read = Column(Boolean, default=False, nullable=False)

    # Relationships
    sender = relationship(
        "User",
        foreign_keys=[sender_id],
        back_populates="sent_messages"
    )
    
    recipient = relationship(
        "User",
        foreign_keys=[recipient_id],
        back_populates="received_messages"
    )

    # Indexes for efficient queries
    __table_args__ = (
        Index('ix_conversation', 'sender_id', 'recipient_id', 'created_at'),
    )

    def __repr__(self):
        return f"<Message(id={self.id}, from={self.sender_id}, to={self.recipient_id})>"
