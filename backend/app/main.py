"""
Main FastAPI application.

Configures:
- CORS middleware
- API routes
- Database initialization
- Startup events
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os

from app.database import init_db, SessionLocal
from app.routes import users, contacts, messages
from app.seed import seed_database

# Create FastAPI app
app = FastAPI(
    title="Sports Messenger API",
    description="Backend API for sports messenger application connecting athletes and officials",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS
# Allow frontend to make requests from different origin
origins = os.getenv("CORS_ORIGINS", "http://localhost:3000").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(users.router, prefix="/api")
app.include_router(contacts.router, prefix="/api")
app.include_router(messages.router, prefix="/api")


@app.on_event("startup")
def startup_event():
    """
    Initialize database and seed data on application startup.
    
    Creates tables if they don't exist and populates with test data.
    """
    print("🚀 Starting Sports Messenger API...")
    
    # Create database tables
    print("📊 Initializing database...")
    init_db()
    
    # Seed database with test data
    db = SessionLocal()
    try:
        seed_database(db)
    finally:
        db.close()
    
    print("✅ Application started successfully!")


@app.get("/")
def root():
    """
    Root endpoint.
    
    Returns API information.
    """
    return {
        "name": "Sports Messenger API",
        "version": "1.0.0",
        "docs": "/docs",
        "status": "running"
    }


@app.get("/health")
def health_check():
    """
    Health check endpoint.
    
    Used to verify API is running properly.
    """
    return {
        "status": "healthy",
        "database": "connected"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
