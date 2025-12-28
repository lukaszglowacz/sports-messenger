"""
Contact service for managing contact exchanges.

Handles logic for:
- Sending contact exchange requests
- Accepting/rejecting requests
- Getting contact lists
- Disconnecting contacts
"""

from sqlalchemy.orm import Session
from sqlalchemy import or_, and_
from datetime import datetime
from typing import List, Dict, Optional
from fastapi import HTTPException

from app.models import User, UserType, ContactExchange, ContactExchangeStatus, Message


class ContactService:
    """
    Service for managing contacts and exchanges.
    
    Implements business rules:
    - Athletes see all other athletes automatically
    - Athletes see officials only after ACCEPTED exchange
    - Officials see only athletes with ACCEPTED exchange
    - Officials never see other officials
    """

    @staticmethod
    def get_contacts_for_user(db: Session, user_id: int) -> Dict:
        """
        Get complete contact list for a user.
        
        Returns different contact lists based on user type:
        - Athletes: See all athletes + officials with ACCEPTED exchange
        - Officials: See only athletes with ACCEPTED exchange
        
        Args:
            db: Database session
            user_id: ID of current user
            
        Returns:
            Dict with keys:
                - contacts: List of users they can message
                - potential_contacts: List of users they could request
                - pending_requests: List of incoming requests
                
        Example:
            >>> result = ContactService.get_contacts_for_user(db, 1)
            >>> for contact in result['contacts']:
            ...     print(f"Can message: {contact['name']}")
        """
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        if user.type == UserType.ATHLETE:
            return ContactService._get_contacts_for_athlete(db, user_id)
        else:
            return ContactService._get_contacts_for_official(db, user_id)

    @staticmethod
    def _get_contacts_for_athlete(db: Session, athlete_id: int) -> Dict:
        """
        Get contacts for an athlete.
        
        Athletes can see:
        1. All other athletes (can message immediately)
        2. Officials with ACCEPTED exchange (can message)
        3. Officials without exchange (can send request)
        """
        contacts = []
        potential_contacts = []

        # 1. Get all other athletes (can always message)
        other_athletes = db.query(User).filter(
            User.type == UserType.ATHLETE,
            User.id != athlete_id
        ).all()

        for athlete in other_athletes:
            # Get last message
            last_msg = ContactService._get_last_message(db, athlete_id, athlete.id)
            
            contacts.append({
                "id": athlete.id,
                "name": athlete.name,
                "type": athlete.type.value,
                "exchange_status": None,
                "exchange_id": None,
                "can_message": True,
                "can_send_request": False,
                "last_message": last_msg.content if last_msg else None,
                "last_message_time": last_msg.created_at if last_msg else None,
                "unread_count": ContactService._get_unread_count(db, athlete_id, athlete.id)
            })

        # 2. Get officials with ACCEPTED exchange
        accepted_exchanges = db.query(ContactExchange, User).join(
            User, ContactExchange.official_id == User.id
        ).filter(
            ContactExchange.athlete_id == athlete_id,
            ContactExchange.status == ContactExchangeStatus.ACCEPTED
        ).all()

        accepted_official_ids = []
        for exchange, official in accepted_exchanges:
            accepted_official_ids.append(official.id)
            last_msg = ContactService._get_last_message(db, athlete_id, official.id)
            
            contacts.append({
                "id": official.id,
                "name": official.name,
                "type": official.type.value,
                "exchange_status": exchange.status.value,
                "exchange_id": exchange.id,
                "can_message": True,
                "can_send_request": False,
                "last_message": last_msg.content if last_msg else None,
                "last_message_time": last_msg.created_at if last_msg else None,
                "unread_count": ContactService._get_unread_count(db, athlete_id, official.id)
            })

        # 3. Get officials WITHOUT exchange (potential contacts)
        all_officials = db.query(User).filter(User.type == UserType.OFFICIAL).all()
        
        for official in all_officials:
            if official.id not in accepted_official_ids:
                # Check if there's a PENDING request
                pending = db.query(ContactExchange).filter(
                    ContactExchange.athlete_id == athlete_id,
                    ContactExchange.official_id == official.id,
                    ContactExchange.status == ContactExchangeStatus.PENDING
                ).first()

                potential_contacts.append({
                    "id": official.id,
                    "name": official.name,
                    "type": official.type.value,
                    "exchange_status": pending.status.value if pending else None,
                    "exchange_id": pending.id if pending else None,
                    "can_message": False,
                    "can_send_request": not pending,
                    "last_message": None,
                    "last_message_time": None,
                    "unread_count": 0
                })

        # Get pending incoming requests
        pending_requests = ContactService._get_pending_requests(db, athlete_id)

        return {
            "contacts": contacts,
            "potential_contacts": potential_contacts,
            "pending_requests": pending_requests
        }

    @staticmethod
    def _get_contacts_for_official(db: Session, official_id: int) -> Dict:
        """
        Get contacts for an official.
        
        Officials can see:
        1. Athletes with ACCEPTED exchange (can message)
        2. Athletes without exchange (can send request)
        3. NO other officials (business rule)
        """
        contacts = []
        potential_contacts = []

        # 1. Get athletes with ACCEPTED exchange
        accepted_exchanges = db.query(ContactExchange, User).join(
            User, ContactExchange.athlete_id == User.id
        ).filter(
            ContactExchange.official_id == official_id,
            ContactExchange.status == ContactExchangeStatus.ACCEPTED
        ).all()

        accepted_athlete_ids = []
        for exchange, athlete in accepted_exchanges:
            accepted_athlete_ids.append(athlete.id)
            last_msg = ContactService._get_last_message(db, official_id, athlete.id)
            
            contacts.append({
                "id": athlete.id,
                "name": athlete.name,
                "type": athlete.type.value,
                "exchange_status": exchange.status.value,
                "exchange_id": exchange.id,
                "can_message": True,
                "can_send_request": False,
                "last_message": last_msg.content if last_msg else None,
                "last_message_time": last_msg.created_at if last_msg else None,
                "unread_count": ContactService._get_unread_count(db, official_id, athlete.id)
            })

        # 2. Get athletes WITHOUT exchange (potential contacts)
        all_athletes = db.query(User).filter(User.type == UserType.ATHLETE).all()
        
        for athlete in all_athletes:
            if athlete.id not in accepted_athlete_ids:
                # Check if there's a PENDING request
                pending = db.query(ContactExchange).filter(
                    ContactExchange.athlete_id == athlete.id,
                    ContactExchange.official_id == official_id,
                    ContactExchange.status == ContactExchangeStatus.PENDING
                ).first()

                potential_contacts.append({
                    "id": athlete.id,
                    "name": athlete.name,
                    "type": athlete.type.value,
                    "exchange_status": pending.status.value if pending else None,
                    "exchange_id": pending.id if pending else None,
                    "can_message": False,
                    "can_send_request": not pending,
                    "last_message": None,
                    "last_message_time": None,
                    "unread_count": 0
                })

        # Get pending incoming requests
        pending_requests = ContactService._get_pending_requests(db, official_id)

        # NOTE: Officials do NOT see other officials at all

        return {
            "contacts": contacts,
            "potential_contacts": potential_contacts,
            "pending_requests": pending_requests
        }

    @staticmethod
    def _get_last_message(db: Session, user1_id: int, user2_id: int) -> Optional[Message]:
        """Get the last message between two users"""
        return db.query(Message).filter(
            or_(
                and_(Message.sender_id == user1_id, Message.recipient_id == user2_id),
                and_(Message.sender_id == user2_id, Message.recipient_id == user1_id)
            )
        ).order_by(Message.created_at.desc()).first()

    @staticmethod
    def _get_unread_count(db: Session, current_user_id: int, other_user_id: int) -> int:
        """Get count of unread messages from other user"""
        return db.query(Message).filter(
            Message.sender_id == other_user_id,
            Message.recipient_id == current_user_id,
            Message.read == False
        ).count()

    @staticmethod
    def _get_pending_requests(db: Session, user_id: int) -> List[Dict]:
        """
        Get pending contact exchange requests for a user.
        
        Returns requests where user is the recipient (to_user).
        """
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            return []

        # Get pending exchanges where user is recipient
        if user.type == UserType.ATHLETE:
            # Athlete receives requests from officials
            pending = db.query(ContactExchange).filter(
                ContactExchange.athlete_id == user_id,
                ContactExchange.status == ContactExchangeStatus.PENDING,
                ContactExchange.initiated_by != user_id
            ).all()
        else:
            # Official receives requests from athletes
            pending = db.query(ContactExchange).filter(
                ContactExchange.official_id == user_id,
                ContactExchange.status == ContactExchangeStatus.PENDING,
                ContactExchange.initiated_by != user_id
            ).all()

        result = []
        for exchange in pending:
            from_user = db.query(User).filter(User.id == exchange.initiated_by).first()
            to_user_id = exchange.official_id if user.type == UserType.ATHLETE else exchange.athlete_id
            to_user = db.query(User).filter(User.id == to_user_id).first()
            
            if from_user and to_user:
                result.append({
                    "exchange_id": exchange.id,
                    "from_user": {
                        "id": from_user.id,
                        "name": from_user.name,
                        "email": from_user.email,
                        "type": from_user.type.value,
                        "created_at": from_user.created_at
                    },
                    "to_user": {
                        "id": to_user.id,
                        "name": to_user.name,
                        "email": to_user.email,
                        "type": to_user.type.value,
                        "created_at": to_user.created_at
                    },
                    "status": exchange.status.value,
                    "created_at": exchange.created_at
                })

        return result

    @staticmethod
    def create_exchange_request(
        db: Session,
        from_user_id: int,
        to_user_id: int
    ) -> ContactExchange:
        """
        Create a new contact exchange request.
        
        Validates:
        - Both users exist
        - One is athlete, one is official
        - No existing exchange exists
        
        Args:
            db: Database session
            from_user_id: User initiating request
            to_user_id: User receiving request
            
        Returns:
            Created ContactExchange object
            
        Raises:
            HTTPException: If validation fails
        """
        from_user = db.query(User).filter(User.id == from_user_id).first()
        to_user = db.query(User).filter(User.id == to_user_id).first()

        if not from_user or not to_user:
            raise HTTPException(status_code=404, detail="User not found")

        # Validate: one must be athlete, one must be official
        if from_user.type == to_user.type:
            raise HTTPException(
                status_code=400,
                detail="Contact exchange only allowed between athlete and official"
            )

        # Determine athlete and official IDs
        athlete_id = from_user_id if from_user.type == UserType.ATHLETE else to_user_id
        official_id = to_user_id if to_user.type == UserType.OFFICIAL else from_user_id

        # Check if exchange already exists
        existing = db.query(ContactExchange).filter(
            ContactExchange.athlete_id == athlete_id,
            ContactExchange.official_id == official_id
        ).first()

        if existing:
            if existing.status == ContactExchangeStatus.ACCEPTED:
                raise HTTPException(
                    status_code=400,
                    detail="Contact already connected"
                )
            elif existing.status == ContactExchangeStatus.PENDING:
                raise HTTPException(
                    status_code=400,
                    detail="Request already pending"
                )
            else:
                # REJECTED - allow new request by deleting old one
                db.delete(existing)
                db.commit()

        # Create new exchange request
        exchange = ContactExchange(
            athlete_id=athlete_id,
            official_id=official_id,
            status=ContactExchangeStatus.PENDING,
            initiated_by=from_user_id,
            created_at=datetime.utcnow()
        )

        db.add(exchange)
        db.commit()
        db.refresh(exchange)

        return exchange

    @staticmethod
    def accept_exchange(db: Session, exchange_id: int, user_id: int) -> ContactExchange:
        """
        Accept a contact exchange request.
        
        Validates that user is the recipient of the request.
        """
        exchange = db.query(ContactExchange).filter(
            ContactExchange.id == exchange_id
        ).first()

        if not exchange:
            raise HTTPException(status_code=404, detail="Exchange not found")

        # Validate user is recipient (not initiator)
        if exchange.initiated_by == user_id:
            raise HTTPException(
                status_code=400,
                detail="Cannot accept your own request"
            )

        # Validate user is part of this exchange
        if user_id != exchange.athlete_id and user_id != exchange.official_id:
            raise HTTPException(
                status_code=403,
                detail="Not authorized to accept this request"
            )

        exchange.status = ContactExchangeStatus.ACCEPTED
        exchange.responded_at = datetime.utcnow()

        db.commit()
        db.refresh(exchange)

        return exchange

    @staticmethod
    def reject_exchange(db: Session, exchange_id: int, user_id: int) -> ContactExchange:
        """
        Reject a contact exchange request.
        
        Validates that user is the recipient of the request.
        """
        exchange = db.query(ContactExchange).filter(
            ContactExchange.id == exchange_id
        ).first()

        if not exchange:
            raise HTTPException(status_code=404, detail="Exchange not found")

        # Validate user is recipient (not initiator)
        if exchange.initiated_by == user_id:
            raise HTTPException(
                status_code=400,
                detail="Cannot reject your own request"
            )

        # Validate user is part of this exchange
        if user_id != exchange.athlete_id and user_id != exchange.official_id:
            raise HTTPException(
                status_code=403,
                detail="Not authorized to reject this request"
            )

        exchange.status = ContactExchangeStatus.REJECTED
        exchange.responded_at = datetime.utcnow()

        db.commit()
        db.refresh(exchange)

        return exchange

    @staticmethod
    def disconnect_contact(db: Session, exchange_id: int, user_id: int) -> bool:
        """
        Disconnect a contact (delete ACCEPTED exchange).
        
        Either user in the exchange can disconnect.
        """
        exchange = db.query(ContactExchange).filter(
            ContactExchange.id == exchange_id
        ).first()

        if not exchange:
            raise HTTPException(status_code=404, detail="Exchange not found")

        # Validate user is part of this exchange
        if user_id != exchange.athlete_id and user_id != exchange.official_id:
            raise HTTPException(
                status_code=403,
                detail="Not authorized to disconnect this contact"
            )

        db.delete(exchange)
        db.commit()

        return True
