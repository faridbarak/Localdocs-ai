"""Main FastAPI application module"""
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from localdocs.api.routes import router
from localdocs.utils.config import settings

# Configure logging dynamically using configuration settings
logging.basicConfig(level=getattr(logging, settings.log_level.upper(), "INFO"))
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events to manage startup and shutdown sequences"""
    # Startup Sequence
    logger.info(f"Starting {settings.app_name} v{settings.app_version}")

    # Verify if local Ollama engine is responsive
    from localdocs.llm.ollama_client import OllamaClient
    client = OllamaClient()
    if not client.check_connection():
        logger.warning("Ollama not running. Documentation generation may fail.")
        logger.info("Install Ollama: curl -fsSL https://ollama.com/install.sh | sh")

    yield

    # Shutdown Sequence
    logger.info(f"Shutting down {settings.app_name}")


app = FastAPI(
    title=settings.app_name,
    description="Privacy-focused local documentation generator using AI",
    version=settings.app_version,
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc"
)

# Include API structural routes seamlessly
app.include_router(router)
