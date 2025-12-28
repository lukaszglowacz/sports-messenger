"""
Contact and exchange API routes.

Endpoints for:
- Getting contact lists
- Sending exchange requests
- Accepting/rejecting requests
- Disconnecting contacts
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas import (
    ContactListResponse,
    ContactExchangeCreate,
    ContactExchangeResponse,
    ContactExchangeAction
)
from app.services.contact_service import ContactService

router = APIRouter(prefix="/contacts", tags=["contacts"])


@router.get("", response_model=ContactListResponse)
def get_contacts(user_id: int, db: Session = Depends(get_db)):
    """
    Get complete contact list for a user.
    
    Returns:
    - contacts: Users they can currently message
    - potential_contacts: Users they could send requests to
    - pending_requests: Incoming requests awaiting response
    
    Args:
        user_id: ID of current user
        
    Returns:
        ContactListResponse: Complete contact information
        
    Example:
        GET /contacts?user_id=1
    """
    return ContactService.get_contacts_for_user(db, user_id)


@router.post("/exchange/request", response_model=ContactExchangeResponse)
def send_exchange_request(
    request: ContactExchangeCreate,
    db: Session = Depends(get_db)
):
    """
    Send a contact exchange request.
    
    Can be initiated by either athlete or official.
    Creates a PENDING exchange that recipient must accept.
    
    Args:
        request: Exchange request details
            - from_user_id: User sending request
            - to_user_id: User receiving request
            
    Returns:
        ContactExchangeResponse: Created exchange
        
    Raises:
        HTTPException(400): If validation fails
        HTTPException(404): If user not found
        
    Example:
        POST /contacts/exchange/request
        {
            "from_user_id": 1,
            "to_user_id": 3
        }
    """
    exchange = ContactService.create_exchange_request(
        db,
        request.from_user_id,
        request.to_user_id
    )
    return exchange


@router.post("/exchange/{exchange_id}/accept", response_model=ContactExchangeResponse)
def accept_exchange_request(
    exchange_id: int,
    action: ContactExchangeAction,
    db: Session = Depends(get_db)
):
    """
    Accept a contact exchange request.
    
    User must be the recipient of the request (not initiator).
    Changes status from PENDING to ACCEPTED.
    
    Args:
        exchange_id: ID of exchange to accept
        action: Action details containing user_id
        
    Returns:
        ContactExchangeResponse: Updated exchange
        
    Raises:
        HTTPException(400): If user is initiator
        HTTPException(403): If user not authorized
        HTTPException(404): If exchange not found
        
    Example:
        POST /contacts/exchange/1/accept
        {
            "user_id": 3
        }
    """
    exchange = ContactService.accept_exchange(db, exchange_id, action.user_id)
    return exchange


@router.post("/exchange/{exchange_id}/reject", response_model=ContactExchangeResponse)
def reject_exchange_request(
    exchange_id: int,
    action: ContactExchangeAction,
    db: Session = Depends(get_db)
):
    """
    Reject a contact exchange request.
    
    User must be the recipient of the request (not initiator).
    Changes status from PENDING to REJECTED.
    User can send new request later.
    
    Args:
        exchange_id: ID of exchange to reject
        action: Action details containing user_id
        
    Returns:
        ContactExchangeResponse: Updated exchange
        
    Raises:
        HTTPException(400): If user is initiator
        HTTPException(403): If user not authorized
        HTTPException(404): If exchange not found
        
    Example:
        POST /contacts/exchange/1/reject
        {
            "user_id": 3
        }
    """
    exchange = ContactService.reject_exchange(db, exchange_id, action.user_id)
    return exchange


@router.delete("/exchange/{exchange_id}")
def disconnect_contact(
    exchange_id: int,
    user_id: int,
    db: Session = Depends(get_db)
):
    """
    Disconnect a contact (delete exchange).
    
    Either user in the exchange can disconnect.
    Deletes the exchange record - users can send new request later.
    
    Args:
        exchange_id: ID of exchange to delete
        user_id: User performing disconnect
        
    Returns:
        dict: Success message
        
    Raises:
        HTTPException(403): If user not authorized
        HTTPException(404): If exchange not found
        
    Example:
        DELETE /contacts/exchange/1?user_id=1
    """
    ContactService.disconnect_contact(db, exchange_id, user_id)
    return {"message": "Contact disconnected successfully"}
