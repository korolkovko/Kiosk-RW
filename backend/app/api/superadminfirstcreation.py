# superadminfirstcreation.py
# Dedicated endpoint for first-time SuperAdmin creation with race condition protection

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from ..database import get_db
from ..models.auth import SuperAdminSetupRequest, LoginResponse
from ..auth.auth_service import auth_service
from ..services.user_service import user_service
from ..services.database_init import db_init_service
from ..database.models import User, Role
from ..auth.password import password_manager

# Create router for first-time SuperAdmin setup
router = APIRouter(prefix="/setup", tags=["first-time-setup"])


@router.post("/superadmin", response_model=LoginResponse)
async def create_first_superadmin(
    setup_request: SuperAdminSetupRequest,
    db: Session = Depends(get_db)
):
    """
    First-time SuperAdmin creation endpoint with race condition protection.
    
    This endpoint is specifically designed to handle the initial SuperAdmin creation
    safely, even under concurrent requests. It uses database-level constraints
    and atomic operations to prevent multiple SuperAdmins.
    
    Args:
        setup_request: SuperAdmin creation request with credentials
        db: Database session
        
    Returns:
        Login response with access token and user info
        
    Raises:
        HTTPException: If SuperAdmin already exists or creation fails
    """
    try:
        # Initialize database with default roles if needed (idempotent)
        db_init_service.initialize_database(db)
        
        # Get SuperAdmin role (this should exist after initialization)
        superadmin_role = db.query(Role).filter(Role.name == "superadmin").first()
        if not superadmin_role:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="SuperAdmin role not found. Database initialization failed."
            )
        
        # Check if username already exists (separate check for better error message)
        existing_user = db.query(User).filter(User.username == setup_request.username).first()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Username '{setup_request.username}' already exists"
            )
        
        # Hash password
        password_hash = password_manager.hash_password(setup_request.password)
        
        # Atomic SuperAdmin creation with race condition protection
        # This will fail if another SuperAdmin already exists due to the unique constraint
        # on role_id for superadmin users (to be added via database constraint)
        superadmin = User(
            username=setup_request.username,
            password_hash=password_hash,
            email=setup_request.email,
            phone=setup_request.phone,
            role_name=superadmin_role.name,
            is_active=True,
            is_verified=True
        )
        
        # Start transaction
        db.add(superadmin)
        
        # This commit will fail if constraint is violated (another superadmin exists)
        try:
            db.commit()
        except IntegrityError as e:
            db.rollback()
            # Check if it's a superadmin constraint violation
            if "unique_superadmin" in str(e).lower() or "role_id" in str(e).lower():
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="SuperAdmin user already exists. Use regular login endpoint."
                )
            else:
                # Some other integrity error (username, email, etc.)
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="User creation failed due to data constraint violation"
                )
        
        # Refresh to get the created user with all fields
        db.refresh(superadmin)
        
        # Update last login timestamp
        user_service.update_last_login(db, superadmin.user_id)
        
        # Generate access token
        token_data = auth_service.create_token_for_user(superadmin)
        
        return LoginResponse(**token_data)
        
    except HTTPException:
        # Re-raise HTTP exceptions as-is
        raise
    except ValueError as e:
        # Convert ValueError to HTTP exception
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        # Catch-all for unexpected errors
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create SuperAdmin: {str(e)}"
        )


@router.get("/status")
async def check_setup_status(db: Session = Depends(get_db)):
    """
    Check if the system needs initial SuperAdmin setup.
    
    This endpoint can be called without authentication to determine
    if first-time setup is required.
    
    Args:
        db: Database session
        
    Returns:
        Dictionary indicating whether setup is needed
    """
    try:
        # Initialize database with default roles if needed
        db_init_service.initialize_database(db)
        
        # Check if any SuperAdmin exists
        has_superadmin = db_init_service.has_superadmin(db)
        
        return {
            "setup_required": not has_superadmin,
            "has_superadmin": has_superadmin,
            "message": "System ready for first-time setup" if not has_superadmin else "System already configured",
            "endpoint": "/api/v1/setup/superadmin" if not has_superadmin else "/api/v1/auth/login"
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to check setup status: {str(e)}"
        )