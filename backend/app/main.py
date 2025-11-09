# app/main.py
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import SQLModel
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from app.core.config import Settings
from app.database.session import engine
from app.core.security import get_current_user
from app.routers import auth, transactions, dashboard, tax, reminders
from app.utils.scheduler import start_scheduler

settings = Settings()

@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator:
    """Async context manager for FastAPI lifespan events"""
    # Startup
    SQLModel.metadata.create_all(engine)
    start_scheduler(settings.REMINDER_CHECK_INTERVAL_SECONDS)
    yield
    # Shutdown
    # Add cleanup code here

app = FastAPI(
    title="BizPilot AI Backend",
    description="Backend API for BizPilot AI Business Management Platform",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs" if settings.DEBUG else None,
    redoc_url="/redoc" if settings.DEBUG else None
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(
    auth.router,
    prefix="/auth",
    tags=["Authentication"]
)
app.include_router(
    transactions.router,
    prefix="/transactions",
    tags=["Transactions"],
    dependencies=[Depends(get_current_user)]
)
app.include_router(
    dashboard.router,
    prefix="/dashboard",
    tags=["Dashboard"],
    dependencies=[Depends(get_current_user)]
)
app.include_router(
    tax.router,
    prefix="/tax",
    tags=["Tax Management"],
    dependencies=[Depends(get_current_user)]
)
app.include_router(
    reminders.router,
    prefix="/reminders",
    tags=["Reminders"],
    dependencies=[Depends(get_current_user)]
)

@app.get("/", tags=["Health Check"])
async def health_check():
    """API health check endpoint"""
    return {
        "status": "healthy",
        "version": settings.VERSION,
        "environment": settings.ENVIRONMENT
    }
