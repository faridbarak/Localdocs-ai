"""Main FastAPI application"""
from fastapi import FastAPI
from contextlib import asynccontextmanager
from localdocs.api.routes import router
from localdocs.utils.config import settings
import logging

# Configure logging
logging.basicConfig(level=getattr(logging, settings.log_level))
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events"""
    # Startup
    logger.info(f"Starting {settings.app_name} v{settings.app_version}")
    
    # Check Ollama connection
    from localdocs.llm.ollama_client import OllamaClient
    client = OllamaClient()
    if not client.check_connection():
        logger.warning("Ollama not running. Documentation generation may fail.")
        logger.info("Install Ollama: curl -fsSL https://ollama.com/install.sh | sh")
    
    yield
    
    # Shutdown
    logger.info("Shutting down LocalDocs AI")


app = FastAPI(
    title=settings.app_name,
    description="Privacy-focused local documentation generator using AI",
    version=settings.app_version,
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc"
)

# Include API router
app.include_router(router)


@app.get("/")
async def root():
    return {
        "app": settings.app_name,
        "version": settings.app_version,
        "docs": "/docs"
    }
