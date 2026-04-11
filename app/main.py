"""
FastAPI application entry point.
Initializes the app, configures middleware, and registers routes.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from contextlib import asynccontextmanager
import logging

from app.config import get_settings
from app.database import create_tables
from app.routes import item_routes
from app.auth import routes as auth_routes

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# Load settings
settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan event handler.
    Runs startup and shutdown logic.
    """
    # Startup: Create database tables
    logger.info(f"Starting {settings.APP_NAME} v{settings.APP_VERSION}")
    create_tables()
    logger.info("Application startup complete")
    
    yield
    
    # Shutdown: Add cleanup logic here if needed
    logger.info("Application shutting down")


# Create FastAPI application
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="""
## Data Listing API

A production-ready REST API for managing items (products, posts, etc.).

### Features:
- ✅ Full CRUD operations (Create, Read, Update, Delete)
- ✅ Pagination support (limit & offset)
- ✅ Search items by title
- ✅ Sorting by price, date, or title
- ✅ Input validation with Pydantic
- ✅ CORS enabled for frontend integration

### Quick Start:
1. Create item: `POST /api/v1/items`
2. List items: `GET /api/v1/items`
3. Get item: `GET /api/v1/items/{id}`
4. Update item: `PUT /api/v1/items/{id}`
5. Delete item: `DELETE /api/v1/items/{id}`
    """,
    lifespan=lifespan,
    docs_url="/docs",  # Swagger UI
    redoc_url="/redoc",  # ReDoc documentation
    openapi_url="/openapi.json",
)

# Configure CORS middleware
# Allows frontend applications to make requests to this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],  # Allow all headers
)

# Include API routes with version prefix
app.include_router(item_routes.router, prefix=settings.API_V1_PREFIX)
app.include_router(auth_routes.router, prefix=settings.API_V1_PREFIX)


@app.get("/", tags=["Health"])
async def root():
    """Health check endpoint."""
    return {
        "name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "running",
        "docs": "/docs",
    }


@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    """Return empty favicon to suppress 404 warnings in development."""
    return Response(status_code=204)


@app.get("/health", tags=["Health"])
async def health_check():
    """Detailed health check endpoint."""
    return {
        "status": "healthy",
        "database": "connected",
        "version": settings.APP_VERSION,
    }


# This allows running with: python -m app.main
if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG,
    )
