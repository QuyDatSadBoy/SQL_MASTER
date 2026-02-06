"""
Main FastAPI application.
Entry point for the Office Building Management System API.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from api.database import create_pool, close_pool
from api.routes import (
    office_routes,
    company_routes,
    rent_contract_routes,
    building_employee_routes,
    report_routes
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for startup and shutdown events."""
    # Startup: Create database connection pool
    await create_pool()
    print("✅ Database connection pool created")
    
    yield
    
    # Shutdown: Close database connection pool
    await close_pool()
    print("✅ Database connection pool closed")


# Create FastAPI application
app = FastAPI(
    title="Office Building Management System",
    description="API for managing office building, companies, contracts, and services",
    version="1.0.0",
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:5174"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Health check endpoint
@app.get("/", tags=["Health"])
async def root():
    """Root endpoint - Health check."""
    return {
        "message": "Office Building Management System API",
        "status": "running",
        "version": "1.0.0"
    }


@app.get("/health", tags=["Health"])
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}


# Include routers
app.include_router(office_routes.router, prefix="/api")
app.include_router(company_routes.router, prefix="/api")
app.include_router(rent_contract_routes.router, prefix="/api")
app.include_router(building_employee_routes.router, prefix="/api")
app.include_router(report_routes.router, prefix="/api")


if __name__ == "__main__":
    import uvicorn
    from api.config import settings
    
    uvicorn.run(
        "api.main:app",
        host=settings.APP_HOST,
        port=settings.APP_PORT,
        reload=settings.DEBUG
    )
