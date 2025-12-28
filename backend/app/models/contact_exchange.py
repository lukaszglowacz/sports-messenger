"""
ContactExchange model.

Represents contact exchanges between athletes and officials.
Only ATHLETE-OFFICIAL pairs can have contact exchanges.
"""

from sqlalchemy import Column, Integer, ForeignKey, Enum as SQLEnum, DateTime, UniqueConstraint
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

from app.database import Base


class ContactExchangeStatus(str, enum.Enum):
    """
    Status of contact exchange request.
    
    PENDING: Request sent, waiting for response
    ACCEPTED: Request accepted, users can now message each other
    REJECTED: Request rejected, can be sent again later
    """
    PENDING = "PENDING"
    ACCEPTED = "ACCEPTED"
    REJECTED = "REJECTED"


class ContactExchange(Base):
    """
    ContactExchange model for athlete-official connections.
    
    This model enforces the business rule that athletes and officials
    must exchange contacts before they can message each other.
    
    Important: Only one exchange record can exist per athlete-official pair
    (enforced by UniqueConstraint).
    
    Attributes:
        id (int): Primary key
        athlete_id (int): Foreign key to User (must be ATHLETE type)
        official_id (int): Foreign key to User (must be OFFICIAL type)
        status (ContactExchangeStatus): Current status of the exchange
        initiated_by (int): User ID who sent the request (can be athlete or official)
        created_at (datetime): When request was created
        responded_at (datetime): When request was accepted/rejected (nullable)
        
    Relationships:
        athlete: The athlete user in this exchange
        official: The official user in this exchange
    """
    __tablename__ = "contact_exchanges"

    id = Column(Integer, primary_key=True, index=True)
    athlete_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    official_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    status = Column(SQLEnum(ContactExchangeStatus), nullable=False, default=ContactExchangeStatus.PENDING)
    initiated_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    responded_at = Column(DateTime, nullable=True)

    # Relationships
    athlete = relationship(
        "User",
        foreign_keys=[athlete_id],
        back_populates="athlete_exchanges"
    )
    
    official = relationship(
        "User",
        foreign_keys=[official_id],
        back_populates="official_exchanges"
    )

    # Ensure only one exchange per athlete-official pair
    __table_args__ = (
        UniqueConstraint('athlete_id', 'official_id', name='uq_athlete_official'),
    )

    def __repr__(self):
        return f"<ContactExchange(id={self.id}, athlete_id={self.athlete_id}, official_id={self.official_id}, status={self.status})>"
