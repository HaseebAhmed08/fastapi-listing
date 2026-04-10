"""
CRUD (Create, Read, Update, Delete) operations for Item model.
Contains all database interaction logic.
"""

from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import Optional
import logging

from app.models import Item
from app.schemas import ItemCreate, ItemUpdate

# Configure logging
logger = logging.getLogger(__name__)


def create_item(db: Session, item: ItemCreate) -> Item:
    """
    Create a new item in the database.
    
    Args:
        db: Database session
        item: Item creation data
        
    Returns:
        Item: Created item instance
    """
    db_item = Item(
        title=item.title,
        description=item.description,
        price=item.price,
    )
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    logger.info(f"Created item: {db_item.title} (ID: {db_item.id})")
    return db_item


def get_item(db: Session, item_id: int) -> Optional[Item]:
    """
    Get a single item by ID.
    
    Args:
        db: Database session
        item_id: Item ID to retrieve
        
    Returns:
        Item: Item instance if found, None otherwise
    """
    return db.query(Item).filter(Item.id == item_id).first()


def get_items(
    db: Session,
    skip: int = 0,
    limit: int = 10,
    search: Optional[str] = None,
    sort_by: Optional[str] = None,
    sort_order: str = "asc",
) -> tuple[list[Item], int]:
    """
    Get a paginated list of items with optional search and sorting.
    
    Args:
        db: Database session
        skip: Number of items to skip (for pagination)
        limit: Maximum number of items to return
        search: Optional search term to filter by title
        sort_by: Field to sort by ('price', 'created_at', 'title')
        sort_order: Sort direction ('asc' or 'desc')
        
    Returns:
        tuple: (List of items, total count)
    """
    # Base query
    query = db.query(Item)
    
    # Apply search filter if provided
    if search:
        search_term = f"%{search}%"
        query = query.filter(Item.title.ilike(search_term))
    
    # Get total count before pagination
    total = query.count()
    
    # Apply sorting if specified
    if sort_by:
        # Map sort field to model column
        sort_columns = {
            "price": Item.price,
            "created_at": Item.created_at,
            "title": Item.title,
        }
        column = sort_columns.get(sort_by)
        if column:
            # Apply ascending or descending order
            order_func = column.asc() if sort_order.lower() == "asc" else column.desc()
            query = query.order_by(order_func)
    else:
        # Default sort by creation date (newest first)
        query = query.order_by(Item.created_at.desc())
    
    # Apply pagination
    items = query.offset(skip).limit(limit).all()
    
    return items, total


def update_item(db: Session, item_id: int, item: ItemUpdate) -> Optional[Item]:
    """
    Update an existing item.
    
    Args:
        db: Database session
        item_id: ID of item to update
        item: Updated item data (only provided fields will be updated)
        
    Returns:
        Item: Updated item instance if found, None otherwise
    """
    db_item = get_item(db, item_id)
    if not db_item:
        return None
    
    # Update only provided fields (partial update)
    update_data = item.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_item, field, value)
    
    db.commit()
    db.refresh(db_item)
    logger.info(f"Updated item: {db_item.title} (ID: {db_item.id})")
    return db_item


def delete_item(db: Session, item_id: int) -> bool:
    """
    Delete an item by ID.
    
    Args:
        db: Database session
        item_id: ID of item to delete
        
    Returns:
        bool: True if deleted, False if not found
    """
    db_item = get_item(db, item_id)
    if not db_item:
        return False
    
    db.delete(db_item)
    db.commit()
    logger.info(f"Deleted item ID: {item_id}")
    return True


def search_items(db: Session, query: str, limit: int = 10) -> list[Item]:
    """
    Search items by title (convenience function).
    
    Args:
        db: Database session
        query: Search term
        limit: Maximum results to return
        
    Returns:
        list[Item]: Matching items
    """
    search_term = f"%{query}%"
    return (
        db.query(Item)
        .filter(Item.title.ilike(search_term))
        .limit(limit)
        .all()
    )
