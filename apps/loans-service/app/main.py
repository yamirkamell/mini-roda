"""Main FastAPI application."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.loans import router as loans_router
from app.api.v1.vehicle_categories import router as vehicle_categories_router
from app.api.v1.vehicles import router as vehicles_router
from app.core.config import settings

app = FastAPI(
    title=settings.api_title,
    description=settings.api_description,
    version=settings.api_version,
    docs_url="/loans/docs",
    redoc_url="/loans/redoc",
    openapi_url="/loans/openapi.json",
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(vehicle_categories_router, prefix="/api/v1")
app.include_router(vehicles_router, prefix="/api/v1")
app.include_router(loans_router, prefix="/api/v1")


@app.get("/", tags=["health"])
async def root() -> dict[str, str]:
    """
    Root endpoint.
    
    Returns:
        Service information
    """
    return {
        "service": "loans-service",
        "status": "running",
        "version": settings.api_version,
    }


@app.get("/health", tags=["health"])
async def health() -> dict[str, str]:
    """
    Health check endpoint.
    
    Returns:
        Health status
    """
    return {"status": "healthy"}


