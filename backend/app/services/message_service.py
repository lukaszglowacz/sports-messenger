"""
Message service containing business logic.

This module implements all business rules for messaging:
- Athlete-athlete messaging (no restrictions except daily limit)
- Athlete-official messaging (requires exchange, has limits)
- Official-official messaging (forbidden)
- Daily message limits
"""

from sqlalchemy.orm import Session
from datetime import datetime, date
from typing import Dict, Optional

from app.models import User, UserType, ContactExchange, ContactExchangeStatus, Message


class MessageValidationService:
    """
    Service for validating message sending permissions.
    
    Implements all business rules defined in requirements:
    1. Athletes can message other athletes freely (max 100/day)
    2. Athletes can message officials only after ACCEPTED exchange (max 5/day per official)
    3. Officials can message athletes only after ACCEPTED exchange (no limit)
    4. Officials CANNOT message other officials
    5. Only text and emojis allowed (validated at API level)
    """

    @staticmethod
    def can_send_message(
        db: Session,
        sender_id: int,
        recipient_id: int
    ) -> Dict:
        """
        Check if sender can send a message to recipient.
        
        Args:
            db: Database session
            sender_id: ID of user sending message
            recipient_id: ID of user receiving message
            
        Returns:
            Dict with keys:
                - allowed (bool): Whether message can be sent
                - reason (str): Human-readable reason if not allowed
                - code (str): Machine-readable error code
                - current (int): Current count (if limit-related)
                - limit (int): Limit value (if limit-related)
                
        Example:
            >>> result = MessageValidationService.can_send_message(db, 1, 2)
            >>> if result['allowed']:
            ...     # Send message
            >>> else:
            ...     # Show error: result['reason']
        """
        # Get users
        sender = db.query(User).filter(User.id == sender_id).first()
        recipient = db.query(User).filter(User.id == recipient_id).first()

        if not sender or not recipient:
            return {
                "allowed": False,
                "reason": "User not found",
                "code": "USER_NOT_FOUND"
            }

        # RULE 1: Officials cannot message other officials
        if sender.type == UserType.OFFICIAL and recipient.type == UserType.OFFICIAL:
            return {
                "allowed": False,
                "reason": "Officials cannot message each other",
                "code": "OFFICIALS_CANNOT_MESSAGE"
            }

        # RULE 2: Athlete to Athlete - always allowed (check daily limit only)
        if sender.type == UserType.ATHLETE and recipient.type == UserType.ATHLETE:
            return MessageValidationService._check_athlete_daily_limit(
                db, sender_id
            )

        # RULE 3: Athlete <-> Official requires ACCEPTED exchange
        if (sender.type == UserType.ATHLETE and recipient.type == UserType.OFFICIAL) or \
           (sender.type == UserType.OFFICIAL and recipient.type == UserType.ATHLETE):
            
            # Determine who is athlete and who is official
            athlete_id = sender_id if sender.type == UserType.ATHLETE else recipient_id
            official_id = recipient_id if recipient.type == UserType.OFFICIAL else sender_id

            # Check if ACCEPTED exchange exists
            exchange = db.query(ContactExchange).filter(
                ContactExchange.athlete_id == athlete_id,
                ContactExchange.official_id == official_id,
                ContactExchange.status == ContactExchangeStatus.ACCEPTED
            ).first()

            if not exchange:
                return {
                    "allowed": False,
                    "reason": "Contact exchange required. Please send a request first.",
                    "code": "EXCHANGE_REQUIRED"
                }

            # If sender is athlete, check limits
            if sender.type == UserType.ATHLETE:
                # Check limit to this specific official (5 per day)
                official_limit_check = MessageValidationService._check_athlete_to_official_limit(
                    db, sender_id, recipient_id
                )
                if not official_limit_check["allowed"]:
                    return official_limit_check

                # Check overall daily limit (100 per day)
                daily_limit_check = MessageValidationService._check_athlete_daily_limit(
                    db, sender_id
                )
                if not daily_limit_check["allowed"]:
                    return daily_limit_check

            # Official sending to athlete - no limits
            return {"allowed": True}

        # Default allow (shouldn't reach here)
        return {"allowed": True}

    @staticmethod
    def _check_athlete_to_official_limit(
        db: Session,
        athlete_id: int,
        official_id: int,
        limit: int = 5
    ) -> Dict:
        """
        Check if athlete has exceeded daily message limit to specific official.
        
        Business rule: Athletes can send max 5 messages per day to each official.
        
        Args:
            db: Database session
            athlete_id: ID of athlete
            official_id: ID of official
            limit: Maximum messages allowed (default: 5)
            
        Returns:
            Dict with allowed status and details
        """
        today = date.today()
        today_start = datetime.combine(today, datetime.min.time())
        today_end = datetime.combine(today, datetime.max.time())

        count = db.query(Message).filter(
            Message.sender_id == athlete_id,
            Message.recipient_id == official_id,
            Message.created_at >= today_start,
            Message.created_at <= today_end
        ).count()

        if count >= limit:
            official = db.query(User).filter(User.id == official_id).first()
            return {
                "allowed": False,
                "reason": f"You have exceeded the daily limit of {limit} messages to {official.name if official else 'this official'}",
                "code": "OFFICIAL_DAILY_LIMIT_EXCEEDED",
                "current": count,
                "limit": limit
            }

        return {"allowed": True, "current": count, "limit": limit}

    @staticmethod
    def _check_athlete_daily_limit(
        db: Session,
        athlete_id: int,
        limit: int = 100
    ) -> Dict:
        """
        Check if athlete has exceeded overall daily message limit.
        
        Business rule: Athletes can send max 100 messages per day total.
        
        Args:
            db: Database session
            athlete_id: ID of athlete
            limit: Maximum messages allowed (default: 100)
            
        Returns:
            Dict with allowed status and details
        """
        today = date.today()
        today_start = datetime.combine(today, datetime.min.time())
        today_end = datetime.combine(today, datetime.max.time())

        count = db.query(Message).filter(
            Message.sender_id == athlete_id,
            Message.created_at >= today_start,
            Message.created_at <= today_end
        ).count()

        if count >= limit:
            return {
                "allowed": False,
                "reason": f"You have exceeded the daily limit of {limit} messages",
                "code": "DAILY_LIMIT_EXCEEDED",
                "current": count,
                "limit": limit
            }

        return {"allowed": True, "current": count, "limit": limit}

    @staticmethod
    def get_message_limits(
        db: Session,
        user_id: int,
        official_id: Optional[int] = None
    ) -> Dict:
        """
        Get current message limits for a user.
        
        Args:
            db: Database session
            user_id: ID of user
            official_id: Optional ID of official (to get specific limit)
            
        Returns:
            Dict with current counts and limits
        """
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            return {
                "total_today": 0,
                "daily_limit": 0,
                "is_exceeded": False
            }

        today = date.today()
        today_start = datetime.combine(today, datetime.min.time())
        today_end = datetime.combine(today, datetime.max.time())

        # Get total messages sent today
        total_today = db.query(Message).filter(
            Message.sender_id == user_id,
            Message.created_at >= today_start,
            Message.created_at <= today_end
        ).count()

        result = {
            "total_today": total_today,
            "daily_limit": 100 if user.type == UserType.ATHLETE else None,
            "is_exceeded": total_today >= 100 if user.type == UserType.ATHLETE else False
        }

        # If checking specific official limit
        if official_id and user.type == UserType.ATHLETE:
            to_official = db.query(Message).filter(
                Message.sender_id == user_id,
                Message.recipient_id == official_id,
                Message.created_at >= today_start,
                Message.created_at <= today_end
            ).count()
            
            result["to_official"] = to_official
            result["official_limit"] = 5

        return result
