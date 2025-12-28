"""
Message API routes.

Endpoints for:
- Sending messages
- Getting conversation history
- Getting message limits
- Validating message permissions
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import or_, and_
from typing import List

from app.database import get_db
from app.models import Message
from app.schemas import (
    MessageCreate,
    MessageResponse,
    MessageLimitsResponse,
    ValidationResponse
)
from app.services.message_service import MessageValidationService

router = APIRouter(prefix="/messages", tags=["messages"])


@router.post("", response_model=MessageResponse, status_code=201)
def send_message(
    message: MessageCreate,
    db: Session = Depends(get_db)
):
    """
    Send a new message.
    
    Validates all business rules before sending:
    - Athletes can message athletes freely (100/day limit)
    - Athletes can message officials after exchange (5/day limit per official)
    - Officials can message athletes after exchange (no limit)
    - Officials cannot message officials
    
    Args:
        message: Message details
            - sender_id: User sending message
            - recipient_id: User receiving message
            - content: Message text (1-1000 chars)
            
    Returns:
        MessageResponse: Created message
        
    Raises:
        HTTPException(400): If validation fails
        HTTPException(429): If limits exceeded
        
    Example:
        POST /messages
        {
            "sender_id": 1,
            "recipient_id": 2,
            "content": "Hello! 👋"
        }
    """
    # Validate message permissions
    validation = MessageValidationService.can_send_message(
        db,
        message.sender_id,
        message.recipient_id
    )

    if not validation["allowed"]:
        status_code = 429 if "LIMIT" in validation.get("code", "") else 400
        raise HTTPException(
            status_code=status_code,
            detail=validation["reason"]
        )

    # Create and save message
    db_message = Message(
        sender_id=message.sender_id,
        recipient_id=message.recipient_id,
        content=message.content
    )

    db.add(db_message)
    db.commit()
    db.refresh(db_message)

    return db_message


@router.get("", response_model=List[MessageResponse])
def get_messages(
    user_id: int,
    contact_id: int,
    db: Session = Depends(get_db)
):
    """
    Get conversation history between two users.
    
    Returns all messages exchanged between user and contact,
    ordered by creation time (oldest first).
    
    Args:
        user_id: Current user ID
        contact_id: Contact user ID
        
    Returns:
        List[MessageResponse]: Messages in conversation
        
    Example:
        GET /messages?user_id=1&contact_id=2
    """
    messages = db.query(Message).filter(
        or_(
            and_(Message.sender_id == user_id, Message.recipient_id == contact_id),
            and_(Message.sender_id == contact_id, Message.recipient_id == user_id)
        )
    ).order_by(Message.created_at.asc()).all()

    # Mark messages as read
    db.query(Message).filter(
        Message.sender_id == contact_id,
        Message.recipient_id == user_id,
        Message.read == False
    ).update({"read": True})
    db.commit()

    return messages


@router.get("/limits", response_model=MessageLimitsResponse)
def get_message_limits(
    user_id: int,
    official_id: int = None,
    db: Session = Depends(get_db)
):
    """
    Get current message limits for a user.
    
    Returns:
    - total_today: Total messages sent today
    - to_official: Messages to specific official today (if official_id provided)
    - daily_limit: Maximum allowed (100 for athletes)
    - official_limit: Maximum per official (5 for athletes)
    - is_exceeded: Whether any limit is exceeded
    
    Args:
        user_id: User to check limits for
        official_id: Optional - check limit to specific official
        
    Returns:
        MessageLimitsResponse: Current limits
        
    Example:
        GET /messages/limits?user_id=1&official_id=3
    """
    limits = MessageValidationService.get_message_limits(db, user_id, official_id)
    return limits


@router.post("/validate", response_model=ValidationResponse)
def validate_message(
    sender_id: int,
    recipient_id: int,
    db: Session = Depends(get_db)
):
    """
    Validate if a message can be sent (without actually sending).
    
    Useful for frontend to check permissions before user types message.
    
    Args:
        sender_id: User who would send message
        recipient_id: User who would receive message
        
    Returns:
        ValidationResponse: Whether allowed and why
        
    Example:
        POST /messages/validate?sender_id=1&recipient_id=3
    """
    validation = MessageValidationService.can_send_message(
        db,
        sender_id,
        recipient_id
    )
    return validation
