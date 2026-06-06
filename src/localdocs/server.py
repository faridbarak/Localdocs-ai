"""
LocalDocs AI Server
===================
FastAPI application with security features
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging

from localdocs.api.routes import router
from localdocs import __version__

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="LocalDocs AI",
    description="Privacy-focused, 100% local documentation generator with security shield",
    version=__version__,
    docs_url="/docs",
    redoc_url="/redoc"
)

# Security: CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8000", "http://127.0.0.1:8000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(router, tags=["API"])

@app.on_event("startup")
async def startup_event():
    """Log startup information"""
    logger.info("="*50)
    logger.info("LocalDocs AI Server Starting")
    logger.info(f"Version: {__version__}")
    logger.info("Security Features: ENABLED")
    logger.info("  - Prompt Injection Protection")
    logger.info("  - Input Validation & Sanitization")
    logger.info("  - Request Logging")
    logger.info("="*50)

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "LocalDocs AI",
        "version": __version__
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "localdocs.server:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
