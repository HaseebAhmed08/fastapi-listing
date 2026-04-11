"""
Item API routes.
Defines all CRUD endpoints for items with pagination, search, and sorting.
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional, Annotated
import logging

from app.database import get_db
from app.schemas import (
    ItemCreate,
    ItemUpdate,
    ItemResponse,
    ItemListResponse,
    MessageResponse,
)
from app import crud

# Configure logging
logger = logging.getLogger(__name__)

# Create router with prefix
router = APIRouter(prefix="/items", tags=["Items"])


@router.post(
    "",
    response_model=ItemResponse,
    status_code=201,
    summary="Create a new item",
    description="Create a new item with title, description, and price.",
)
def create_item(item: ItemCreate, db: Session = Depends(get_db)):
    """
    Create a new item.
    
    - **title**: Item title (required, 1-255 characters)
    - **description**: Item description (optional, max 1000 characters)
    - **price**: Item price (required, must be > 0)
    """
    try:
        return crud.create_item(db=db, item=item)
    except Exception as e:
        logger.error(f"Error creating item: {e}")
        raise HTTPException(status_code=500, detail="Failed to create item")


@router.get(
    "",
    response_model=ItemListResponse,
    summary="Get all items",
    description="Retrieve a paginated list of items with optional search and sorting.",
)
def get_items(
    skip: int = Query(0, ge=0, description="Number of items to skip"),
    limit: int = Query(10, ge=1, le=100, description="Maximum items to return"),
    search: Optional[str] = Query(None, description="Search items by title"),
    sort_by: Optional[str] = Query(
        None, description="Sort by field (price, created_at, title)"
    ),
    sort_order: str = Query("asc", pattern="^(asc|desc)$", description="Sort order (asc or desc)"),
    db: Session = Depends(get_db),
):
    """
    Get all items with pagination, search, and sorting.
    
    - **skip**: Number of items to skip (default: 0)
    - **limit**: Maximum items to return, 1-100 (default: 10)
    - **search**: Optional search term to filter by title
    - **sort_by**: Field to sort by (price, created_at, title)
    - **sort_order**: Sort direction (asc or desc)
    """
    try:
        items, total = crud.get_items(
            db=db,
            skip=skip,
            limit=limit,
            search=search,
            sort_by=sort_by,
            sort_order=sort_order,
        )
        return ItemListResponse(
            items=items,
            total=total,
            limit=limit,
            offset=skip,
        )
    except Exception as e:
        logger.error(f"Error fetching items: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch items")


@router.get(
    "/{item_id}",
    response_model=ItemResponse,
    summary="Get item by ID",
    description="Retrieve a single item by its unique identifier.",
)
def get_item(item_id: int, db: Session = Depends(get_db)):
    """
    Get a single item by ID.
    
    - **item_id**: Unique identifier of the item
    """
    db_item = crud.get_item(db=db, item_id=item_id)
    if not db_item:
        raise HTTPException(status_code=404, detail=f"Item with ID {item_id} not found")
    return db_item


@router.put(
    "/{item_id}",
    response_model=ItemResponse,
    summary="Update an item",
    description="Update an existing item by its ID. Only provided fields will be updated.",
)
def update_item(item_id: int, item: ItemUpdate, db: Session = Depends(get_db)):
    """
    Update an existing item.
    
    - **item_id**: ID of the item to update
    - **title**: Updated title (optional)
    - **description**: Updated description (optional)
    - **price**: Updated price (optional, must be > 0)
    """
    try:
        updated_item = crud.update_item(db=db, item_id=item_id, item=item)
        if not updated_item:
            raise HTTPException(
                status_code=404, detail=f"Item with ID {item_id} not found"
            )
        return updated_item
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating item {item_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to update item")


@router.delete(
    "/{item_id}",
    response_model=MessageResponse,
    summary="Delete an item",
    description="Delete an item by its ID.",
)
def delete_item(item_id: int, db: Session = Depends(get_db)):
    """
    Delete an item by ID.
    
    - **item_id**: ID of the item to delete
    """
    try:
        deleted = crud.delete_item(db=db, item_id=item_id)
        if not deleted:
            raise HTTPException(
                status_code=404, detail=f"Item with ID {item_id} not found"
            )
        return MessageResponse(
            message=f"Item with ID {item_id} deleted successfully",
            status_code=200,
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting item {item_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to delete item")


@router.post(
    "/seed",
    response_model=MessageResponse,
    summary="Seed dummy data",
    description="Populate the database with dummy items for testing.",
)
def seed_data(db: Session = Depends(get_db)):
    """
    Seed the database with 10 dummy items.
    Useful for testing and development.
    """
    from app.schemas import ItemCreate as IC

    dummy_items = [
        IC(title="Laptop Pro 15", description="High-performance laptop with 15-inch display, 16GB RAM, 512GB SSD", price=1299.99),
        IC(title="Wireless Mouse", description="Ergonomic wireless mouse with long battery life", price=29.99),
        IC(title="USB-C Hub", description="7-in-1 USB-C hub with HDMI, USB 3.0, and SD card reader", price=49.99),
        IC(title="Mechanical Keyboard", description="RGB mechanical keyboard with Cherry MX Blue switches", price=89.99),
        IC(title="Monitor 27 inch", description="4K IPS monitor with 144Hz refresh rate and HDR support", price=449.99),
        IC(title="Webcam HD", description="1080p webcam with built-in microphone and auto light correction", price=59.99),
        IC(title="Desk Lamp", description="LED desk lamp with adjustable brightness and color temperature", price=34.99),
        IC(title="Bluetooth Speaker", description="Portable waterproof speaker with 12-hour battery life", price=79.99),
        IC(title="Phone Stand", description="Adjustable aluminum stand for smartphones and tablets", price=14.99),
        IC(title="External SSD 1TB", description="Ultra-fast portable SSD with USB 3.2 Gen 2 support", price=109.99),
    ]

    count = 0
    for item_data in dummy_items:
        crud.create_item(db=db, item=item_data)
        count += 1

    return MessageResponse(message=f"Seeded {count} dummy items successfully!", status_code=201)
