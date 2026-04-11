"""
Seed script to populate the database with dummy data.
Run: python -m app.seed
"""

import logging
from app.database import get_db_context
from app.crud import create_item
from app.schemas import ItemCreate

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

DUMMY_ITEMS = [
    ItemCreate(
        title="Laptop Pro 15",
        description="High-performance laptop with 15-inch display, 16GB RAM, 512GB SSD",
        price=1299.99,
    ),
    ItemCreate(
        title="Wireless Mouse",
        description="Ergonomic wireless mouse with long battery life",
        price=29.99,
    ),
    ItemCreate(
        title="USB-C Hub",
        description="7-in-1 USB-C hub with HDMI, USB 3.0, and SD card reader",
        price=49.99,
    ),
    ItemCreate(
        title="Mechanical Keyboard",
        description="RGB mechanical keyboard with Cherry MX Blue switches",
        price=89.99,
    ),
    ItemCreate(
        title="Monitor 27 inch",
        description="4K IPS monitor with 144Hz refresh rate and HDR support",
        price=449.99,
    ),
    ItemCreate(
        title="Webcam HD",
        description="1080p webcam with built-in microphone and auto light correction",
        price=59.99,
    ),
    ItemCreate(
        title="Desk Lamp",
        description="LED desk lamp with adjustable brightness and color temperature",
        price=34.99,
    ),
    ItemCreate(
        title="Bluetooth Speaker",
        description="Portable waterproof speaker with 12-hour battery life",
        price=79.99,
    ),
    ItemCreate(
        title="Phone Stand",
        description="Adjustable aluminum stand for smartphones and tablets",
        price=14.99,
    ),
    ItemCreate(
        title="External SSD 1TB",
        description="Ultra-fast portable SSD with USB 3.2 Gen 2 support",
        price=109.99,
    ),
]


def seed():
    """Insert dummy items into the database."""
    with get_db_context() as db:
        for item_data in DUMMY_ITEMS:
            create_item(db, item_data)
            logger.info(f"Seeded: {item_data.title}")

    logger.info(f"Successfully seeded {len(DUMMY_ITEMS)} items!")


if __name__ == "__main__":
    seed()
