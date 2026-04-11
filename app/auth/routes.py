"""
Authentication routes (login, signup, token refresh).
Provides API endpoints for user authentication.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from typing import Annotated

from app.database import get_db
from app.auth.schemas import UserRegister, UserLogin, TokenResponse, UserResponse
from app.auth import crud

router = APIRouter(prefix="/auth", tags=["Authentication"])

# Bearer token scheme
security = HTTPBearer()


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new user",
    description="Create a new user account with username, email, and password."
)
async def register(user_data: UserRegister, db: Annotated[Session, Depends(get_db)]):
    """
    Register a new user.

    - **username**: Unique username (3-50 characters)
    - **email**: Valid email address
    - **password**: Password (min 6 characters)
    """
    try:
        user = crud.register_user(db, user_data)
        return user
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.post(
    "/login",
    response_model=TokenResponse,
    summary="Login user",
    description="Authenticate with email and password to receive JWT tokens."
)
async def login(login_data: UserLogin, db: Annotated[Session, Depends(get_db)]):
    """
    Authenticate user and return JWT tokens.

    - **email**: User email address
    - **password**: User password

    Returns access_token and refresh_token.
    """
    # Authenticate user
    user = crud.authenticate_user(db, login_data.email, login_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Create tokens
    token_data = {"sub": str(user.id), "email": user.email}
    access_token = crud.create_access_token(data=token_data)
    refresh_token = crud.create_refresh_token(data=token_data)

    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer"
    )


@router.post(
    "/refresh",
    response_model=TokenResponse,
    summary="Refresh access token",
    description="Use a refresh token to get a new access token."
)
async def refresh_token(refresh_token: str, db: Annotated[Session, Depends(get_db)]):
    """
    Refresh an access token using a refresh token.

    - **refresh_token**: JWT refresh token received during login
    """
    # Decode and validate refresh token
    payload = crud.decode_token(refresh_token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired refresh token",
        )

    # Get user from token
    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload",
        )

    user = crud.get_user_by_id(db, int(user_id))
    if not user or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found or inactive",
        )

    # Create new access token
    token_data = {"sub": str(user.id), "email": user.email}
    new_access_token = crud.create_access_token(data=token_data)

    return TokenResponse(
        access_token=new_access_token,
        refresh_token=refresh_token,
        token_type="bearer"
    )


@router.get(
    "/me",
    response_model=UserResponse,
    summary="Get current user profile",
    description="Retrieve the authenticated user's profile information."
)
async def get_current_user(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],
    db: Annotated[Session, Depends(get_db)]
):
    """
    Get current authenticated user's profile.

    Requires Bearer token in Authorization header.
    """
    token = credentials.credentials
    payload = crud.decode_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        )

    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload",
        )

    user = crud.get_user_by_id(db, int(user_id))
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    return user
