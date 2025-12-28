"""
Pydantic schemas for request/response validation.

These schemas define the structure of data sent to and from the API.
They provide automatic validation and documentation.
"""

from pydantic import BaseModel, EmailStr, Field, field_validator
from datetime import datetime
from typing import Optional, List
from enum import Enum


# Enums matching database enums
class UserTypeSchema(str, Enum):
    """User type enum for API schemas"""
    ATHLETE = "ATHLETE"
    OFFICIAL = "OFFICIAL"


class ContactExchangeStatusSchema(str, Enum):
    """Contact exchange status enum for API schemas"""
    PENDING = "PENDING"
    ACCEPTED = "ACCEPTED"
    REJECTED = "REJECTED"


# User schemas
class UserBase(BaseModel):
    """Base user schema with common fields"""
    name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr
    type: UserTypeSchema


class UserCreate(UserBase):
    """Schema for creating a new user"""
    pass


class UserResponse(UserBase):
    """Schema for user responses"""
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


# Message schemas
class MessageCreate(BaseModel):
    """
    Schema for creating a new message.
    
    Validates:
    - sender_id and recipient_id are provided
    - content is text only (1-1000 chars)
    """
    sender_id: int = Field(..., gt=0)
    recipient_id: int = Field(..., gt=0)
    content: str = Field(..., min_length=1, max_length=1000)

    @field_validator('content')
    @classmethod
    def validate_text_only(cls, v: str) -> str:
        """
        Validate that content is text and emojis only.
        
        This is a basic validation - frontend should also prevent
        file uploads and image pasting.
        """
        if not v.strip():
            raise ValueError("Message cannot be empty")
        return v.strip()


class MessageResponse(BaseModel):
    """Schema for message responses"""
    id: int
    sender_id: int
    recipient_id: int
    content: str
    created_at: datetime
    read: bool

    class Config:
        from_attributes = True


# Contact Exchange schemas
class ContactExchangeCreate(BaseModel):
    """
    Schema for creating a contact exchange request.
    
    Either athlete or official can initiate the exchange.
    """
    from_user_id: int = Field(..., gt=0, description="User initiating the request")
    to_user_id: int = Field(..., gt=0, description="User receiving the request")


class ContactExchangeResponse(BaseModel):
    """Schema for contact exchange responses"""
    id: int
    athlete_id: int
    official_id: int
    status: ContactExchangeStatusSchema
    initiated_by: int
    created_at: datetime
    responded_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class ContactExchangeAction(BaseModel):
    """Schema for accepting/rejecting exchange requests"""
    user_id: int = Field(..., gt=0, description="User performing the action")


# Contact list schemas
class ContactInfo(BaseModel):
    """
    Information about a contact in user's contact list.
    
    Includes exchange status for officials, and whether user can message them.
    """
    id: int
    name: str
    type: UserTypeSchema
    exchange_status: Optional[ContactExchangeStatusSchema] = None
    exchange_id: Optional[int] = None
    can_message: bool
    can_send_request: bool
    last_message: Optional[str] = None
    last_message_time: Optional[datetime] = None
    unread_count: int = 0


class PendingRequestInfo(BaseModel):
    """Information about a pending contact exchange request"""
    exchange_id: int
    from_user: UserResponse
    to_user: UserResponse
    status: ContactExchangeStatusSchema
    created_at: datetime


class ContactListResponse(BaseModel):
    """
    Complete contact list for a user.
    
    Includes:
    - contacts: Users they can currently message
    - potential_contacts: Users they could request to message
    - pending_requests: Incoming requests awaiting response
    """
    contacts: List[ContactInfo]
    potential_contacts: List[ContactInfo]
    pending_requests: List[PendingRequestInfo]


# Message limits schemas
class MessageLimitsResponse(BaseModel):
    """
    Current message limits for a user.
    
    Tracks:
    - total_today: Total messages sent today
    - to_official: Messages sent to specific official today (if applicable)
    - daily_limit: Maximum allowed (100 for athletes, None for officials)
    - official_limit: Maximum to one official (5 for athletes, None for officials)
    """
    total_today: int
    to_official: Optional[int] = None
    daily_limit: Optional[int] = None
    official_limit: Optional[int] = None
    is_exceeded: bool


# Validation response
class ValidationResponse(BaseModel):
    """
    Response from message validation.
    
    Indicates whether user can send a message and why/why not.
    """
    allowed: bool
    reason: Optional[str] = None
    code: Optional[str] = None
    current: Optional[int] = None
    limit: Optional[int] = None


# Conversation schema
class ConversationResponse(BaseModel):
    """Information about a conversation between two users"""
    contact: ContactInfo
    messages: List[MessageResponse]
    can_send: bool
    validation: Optional[ValidationResponse] = None
