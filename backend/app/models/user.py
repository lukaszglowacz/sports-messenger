"""
User model.

Represents users in the system - both athletes and officials (managers).
"""

from sqlalchemy import Column, Integer, String, Enum as SQLEnum, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

from app.database import Base


class UserType(str, enum.Enum):
    """
    Enum defining types of users in the system.
    
    ATHLETE: Players/competitors who can message other athletes freely
             and officials only after contact exchange
    OFFICIAL: Managers/coaches who can message athletes only after
              contact exchange, cannot message other officials
    """
    ATHLETE = "ATHLETE"
    OFFICIAL = "OFFICIAL"


class User(Base):
    """
    User model representing both athletes and officials.
    
    Attributes:
        id (int): Primary key
        name (str): User's display name
        email (str): User's email address (unique)
        type (UserType): Whether user is ATHLETE or OFFICIAL
        created_at (datetime): When user was created
        
    Relationships:
        sent_messages: Messages sent by this user
        received_messages: Messages received by this user
        athlete_exchanges: Contact exchanges where user is athlete
        official_exchanges: Contact exchanges where user is official
    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    type = Column(SQLEnum(UserType), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    sent_messages = relationship(
        "Message",
        foreign_keys="Message.sender_id",
        back_populates="sender",
        cascade="all, delete-orphan"
    )
    
    received_messages = relationship(
        "Message",
        foreign_keys="Message.recipient_id",
        back_populates="recipient",
        cascade="all, delete-orphan"
    )
    
    # Contact exchanges where this user is the athlete
    athlete_exchanges = relationship(
        "ContactExchange",
        foreign_keys="ContactExchange.athlete_id",
        back_populates="athlete",
        cascade="all, delete-orphan"
    )
    
    # Contact exchanges where this user is the official
    official_exchanges = relationship(
        "ContactExchange",
        foreign_keys="ContactExchange.official_id",
        back_populates="official",
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<User(id={self.id}, name='{self.name}', type={self.type})>"
