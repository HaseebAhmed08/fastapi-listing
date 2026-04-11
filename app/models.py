"""
SQLAlchemy database models.
Defines the structure of database tables.
"""

from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean
from sqlalchemy.sql import func
from app.database import Base


class User(Base):
    """
    User model for authentication.

    Attributes:
        id: Primary key (auto-increment)
        username: Unique username (required)
        email: Unique email address (required)
        hashed_password: Bcrypt hashed password
        is_active: Account status flag
        created_at: Timestamp of creation
        updated_at: Timestamp of last update
    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}', email='{self.email}')>"


class Item(Base):
    """
    Item model representing a product or data entry.
    
    Attributes:
        id: Primary key (auto-increment)
        title: Item title (required, indexed for faster searches)
        description: Optional detailed description
        price: Item price (must be positive)
        created_at: Timestamp of creation (auto-set)
        updated_at: Timestamp of last update (auto-set)
    """
    __tablename__ = "items"
    
    # Primary key
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    
    # Title - required, indexed for search performance
    title = Column(String(255), nullable=False, index=True)
    
    # Description - optional, can be null
    description = Column(String(1000), nullable=True)
    
    # Price - must be positive (enforced at application level)
    price = Column(Float, nullable=False, default=0.0)
    
    # Timestamps - automatically managed
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    def __repr__(self):
        """String representation for debugging."""
        return f"<Item(id={self.id}, title='{self.title}', price={self.price})>"
