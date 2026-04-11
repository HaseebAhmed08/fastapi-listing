"""
Pydantic schemas for authentication.
Defines request and response models for login/signup.
"""

from pydantic import BaseModel, EmailStr, Field
from typing import Optional


class UserRegister(BaseModel):
    """Schema for user registration."""
    username: str = Field(
        ...,
        min_length=3,
        max_length=50,
        description="Unique username",
        examples=["johndoe"]
    )
    email: EmailStr = Field(
        ...,
        description="User email address",
        examples=["john@example.com"]
    )
    password: str = Field(
        ...,
        min_length=6,
        max_length=100,
        description="User password (min 6 characters)",
        examples=["securepass123"]
    )


class UserLogin(BaseModel):
    """Schema for user login."""
    email: EmailStr = Field(
        ...,
        description="User email address",
        examples=["john@example.com"]
    )
    password: str = Field(
        ...,
        description="User password",
        examples=["securepass123"]
    )


class TokenResponse(BaseModel):
    """Schema for JWT token response."""
    access_token: str = Field(..., description="JWT access token")
    refresh_token: Optional[str] = Field(None, description="JWT refresh token")
    token_type: str = Field(default="bearer", description="Token type")


class UserResponse(BaseModel):
    """Schema for user profile response."""
    id: int
    username: str
    email: str
    is_active: bool

    class Config:
        from_attributes = True
