# users.py
# User management endpoints (only accessible by SuperAdmin)

from fastapi import APIRouter, Depends, HTTPException, status, Body
from sqlalchemy.orm import Session
from typing import List

from ..database import get_db
from ..models.user import UserCreate, UserResponse, UserUpdate, AdminCreate
from ..auth import get_current_superadmin
from ..services.user_service import user_service
from ..database.models import User, Role
from ..auth.password import password_manager

# Create router for user management endpoints
router = APIRouter(prefix="/users", tags=["user-management"])


@router.post("/create-admin", response_model=UserResponse)
async def create_admin_user(
    user_data: AdminCreate,
    current_user: User = Depends(get_current_superadmin),
    db: Session = Depends(get_db)
):
    """
    Create a new Admin user. Only accessible by SuperAdmin.
    
    Logic:
    1. Verify requester is SuperAdmin (handled by dependency)
    2. Check if 'admin' role exists in roles table
    3. Assign admin role_name from roles table to new user (ignores role_id in request)
    4. Return success/failure message
    
    Args:
        user_data: User creation data (role_id field is ignored - admin role assigned automatically)
        current_user: Current SuperAdmin user (verified)
        db: Database session
        
    Returns:
        Created admin user information
        
    Raises:
        HTTPException: If admin role not found or user creation fails
    """
    try:
        # Check if 'admin' role exists
        admin_role = db.query(Role).filter(Role.name == "admin").first()
        if not admin_role:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No such role 'admin' found in roles table"
            )
        
        # Check if username already exists
        existing_user = db.query(User).filter(User.username == user_data.username).first()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Username '{user_data.username}' already exists"
            )
        
        # Hash password
        password_hash = password_manager.hash_password(user_data.password)
        
        # Create admin user with admin role_name (ignore role_id from request)
        admin_user = User(
            username=user_data.username,
            password_hash=password_hash,
            email=user_data.email,
            phone=user_data.phone,
            role_name=admin_role.name,  # Always assign admin role from roles table
            is_active=user_data.is_active,
            is_verified=user_data.is_verified
        )
        
        db.add(admin_user)
        db.commit()
        db.refresh(admin_user)
        
        return UserResponse.model_validate(admin_user)
        
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create admin user: {str(e)}"
        )


@router.get("/", response_model=List[UserResponse])
async def get_users(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_superadmin),
    db: Session = Depends(get_db)
):
    """
    Get list of all users. Only accessible by SuperAdmin.
    
    Args:
        skip: Number of records to skip (for pagination)
        limit: Maximum number of records to return
        current_user: Current SuperAdmin user
        db: Database session
        
    Returns:
        List of users
    """
    users = user_service.get_users(db=db, skip=skip, limit=limit)
    return [UserResponse.model_validate(user) for user in users]


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: int,
    current_user: User = Depends(get_current_superadmin),
    db: Session = Depends(get_db)
):
    """
    Get user by ID. Only accessible by SuperAdmin.
    
    Args:
        user_id: User ID to retrieve
        current_user: Current SuperAdmin user
        db: Database session
        
    Returns:
        User information
        
    Raises:
        HTTPException: If user not found
    """
    user = user_service.get_user_by_id(db=db, user_id=user_id)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with ID {user_id} not found"
        )
    
    return UserResponse.model_validate(user)


@router.put("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: int,
    user_update: UserUpdate,
    current_user: User = Depends(get_current_superadmin),
    db: Session = Depends(get_db)
):
    """
    Update user by ID. Only accessible by SuperAdmin.
    
    Args:
        user_id: User ID to update
        user_update: User update data
        current_user: Current SuperAdmin user
        db: Database session
        
    Returns:
        Updated user information
        
    Raises:
        HTTPException: If user not found or update fails
    """
    try:
        updated_user = user_service.update_user(
            db=db, 
            user_id=user_id, 
            user_update=user_update
        )
        
        if not updated_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with ID {user_id} not found"
            )
        
        return UserResponse.model_validate(updated_user)
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update user: {str(e)}"
        )


@router.delete("/{user_id}")
async def delete_user(
    user_id: int,
    current_user: User = Depends(get_current_superadmin),
    db: Session = Depends(get_db)
):
    """
    Delete user by ID. Only accessible by SuperAdmin.
    
    Args:
        user_id: User ID to delete
        current_user: Current SuperAdmin user
        db: Database session
        
    Returns:
        Confirmation message
        
    Raises:
        HTTPException: If user not found or cannot be deleted
    """
    # Prevent SuperAdmin from deleting themselves
    if user_id == current_user.user_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot delete your own account"
        )
    
    # Attempt to delete user
    success = user_service.delete_user(db=db, user_id=user_id)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with ID {user_id} not found"
        )
    
    return {"message": f"User with ID {user_id} has been deleted successfully"}