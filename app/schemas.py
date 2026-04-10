"""
Pydantic schemas for request validation and response serialization.
Defines the structure of API request bodies and responses.
"""

from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime


class ItemBase(BaseModel):
    """
    Base schema with common item fields.
    Used as parent for Create and Update schemas.
    """
    title: str = Field(
        ...,
        min_length=1,
        max_length=255,
        description="Item title (required)",
        examples=["Laptop Pro 15"]
    )
    description: Optional[str] = Field(
        None,
        max_length=1000,
        description="Optional item description",
        examples=["High-performance laptop with 15-inch display"]
    )
    price: float = Field(
        ...,
        gt=0,
        description="Item price (must be greater than 0)",
        examples=[999.99]
    )


class ItemCreate(ItemBase):
    """
    Schema for creating a new item.
    Inherits all fields from ItemBase.
    """
    pass


class ItemUpdate(BaseModel):
    """
    Schema for updating an existing item.
    All fields are optional to allow partial updates.
    """
    title: Optional[str] = Field(
        None,
        min_length=1,
        max_length=255,
        description="Item title",
        examples=["Updated Laptop Pro 15"]
    )
    description: Optional[str] = Field(
        None,
        max_length=1000,
        description="Item description",
        examples=["Updated description"]
    )
    price: Optional[float] = Field(
        None,
        gt=0,
        description="Item price (must be greater than 0)",
        examples=[1099.99]
    )


class ItemResponse(ItemBase):
    """
    Schema for item responses.
    Includes database-generated fields (id, timestamps).
    """
    model_config = ConfigDict(from_attributes=True)  # Enable ORM mode
    
    id: int = Field(..., description="Unique item identifier", examples=[1])
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")


class ItemListResponse(BaseModel):
    """
    Paginated response schema for item list.
    Includes metadata for pagination.
    """
    items: list[ItemResponse]
    total: int = Field(..., description="Total number of items", examples=[100])
    limit: int = Field(..., description="Items per page", examples=[10])
    offset: int = Field(..., description="Number of items skipped", examples=[0])
    
    @property
    def has_more(self) -> bool:
        """Check if there are more items to fetch."""
        return self.offset + self.limit < self.total


class ErrorResponse(BaseModel):
    """Standard error response schema."""
    error: str = Field(..., description="Error type")
    message: str = Field(..., description="Detailed error message")
    status_code: int = Field(..., description="HTTP status code")


class MessageResponse(BaseModel):
    """Simple message response for operations like delete."""
    message: str = Field(..., description="Operation result message")
    status_code: int = Field(..., description="HTTP status code")
