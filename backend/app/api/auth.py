# auth.py
# Authentication endpoints for login, logout, and initial setup

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Dict, Any

from ..database import get_db
from ..models.auth import LoginRequest, LoginResponse, LogoutResponse
from ..models.user import UserResponse
from ..auth import get_current_user
from ..auth.auth_service import auth_service
from ..services.user_service import user_service
from ..database.models import User

# Create router for authentication endpoints
router = APIRouter(prefix="/auth", tags=["authentication"])



@router.post("/login", response_model=LoginResponse)
async def login(
    login_request: LoginRequest,
    db: Session = Depends(get_db)
):
    """
    Standard login endpoint for existing users.
    
    Args:
        login_request: Login credentials (username and password)
        db: Database session
        
    Returns:
        Login response with access token and user info
        
    Raises:
        HTTPException: If credentials are invalid
    """
    # Authenticate user
    user = auth_service.authenticate_user(
        db=db,
        username=login_request.username,
        password=login_request.password
    )
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Update last login timestamp
    user_service.update_last_login(db, user.user_id)
    
    # Generate access token
    token_data = auth_service.create_token_for_user(user)
    
    return LoginResponse(**token_data)


@router.post("/logout", response_model=LogoutResponse)
async def logout(
    current_user: User = Depends(get_current_user)
):
    """
    Logout endpoint for authenticated users.
    Since we're using stateless JWT tokens, this endpoint primarily serves
    as a confirmation that the user wants to logout. The actual logout
    happens on the client side by discarding the token.
    
    Args:
        current_user: Current authenticated user
        
    Returns:
        Logout confirmation message
    """
    return LogoutResponse(message=f"User {current_user.username} successfully logged out")


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(
    current_user: User = Depends(get_current_user)
):
    """
    Get current user information.
    
    Args:
        current_user: Current authenticated user
        
    Returns:
        Current user information
    """
    return UserResponse.model_validate(current_user)


