"""
User API routes.

Endpoints for user management.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models import User
from app.schemas import UserResponse

router = APIRouter(prefix="/users", tags=["users"])


@router.get("", response_model=List[UserResponse])
def get_all_users(db: Session = Depends(get_db)):
    """
    Get all users in the system.
    
    Returns list of all users (athletes and officials).
    Used by frontend for user switcher dropdown.
    
    Returns:
        List[UserResponse]: All users
    """
    users = db.query(User).all()
    return users


@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    """
    Get a specific user by ID.
    
    Args:
        user_id: ID of user to retrieve
        
    Returns:
        UserResponse: User details
        
    Raises:
        HTTPException(404): If user not found
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
