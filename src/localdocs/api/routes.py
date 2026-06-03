"""API routes for LocalDocs AI"""
from fastapi import APIRouter, HTTPException
from localdocs.api.schemas import (
    GenerateDocsRequest,
    GenerateDocsResponse,
    HealthCheckResponse
)
from localdocs.llm.ollama_client import OllamaClient
from localdocs.parsers.python_parser import PythonParser
from localdocs.generators.markdown_generator import MarkdownGenerator
from localdocs.utils.config import settings

router = APIRouter()
ollama_client = OllamaClient()


@router.get("/")
async def root():
    return {
        "message": "Welcome to LocalDocs AI",
        "version": settings.app_version,
        "docs": "/docs"
    }


@router.get("/api/v1/health", response_model=HealthCheckResponse)
async def health_check():
    return HealthCheckResponse(
        status="healthy",
        version=settings.app_version,
        ollama_connected=ollama_client.check_connection()
    )


@router.get("/api/v1/models")
async def list_models():
    """List available Ollama models"""
    # Safe placeholder until list_models is implemented in the client
    try:
        return {"models": [settings.default_model], "default": settings.default_model}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/api/v1/generate-docs", response_model=GenerateDocsResponse)
async def generate_docs(request: GenerateDocsRequest):
    """Generate documentation for code"""
    try:
        # Parse code
        parser = PythonParser(request.code)
        elements = parser.parse()
        
        # Generate AI documentation using aligned client parameters
        ai_docs = ollama_client.generate_docs(
            code=request.code,
            model=request.model
        )
        
        # Combine parsed + AI docs
        markdown = MarkdownGenerator.generate(elements, request.project_name)
        markdown += "\n\n## AI-Generated Documentation\n\n"
        markdown += ai_docs
        
        return GenerateDocsResponse(
            success=True,
            documentation=markdown,
            elements_count=len(elements),
            model_used=request.model or settings.default_model
        )
        
    except ConnectionError as e:
        raise HTTPException(status_code=503, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


@router.post("/api/v1/parse-code")
async def parse_code(code: str, language: str = "python"):
    """Parse code without generating docs"""
    if language.lower() == "python":
        parser = PythonParser(code)
        elements = parser.parse()
        return {
            "success": True,
            "elements": [
                {"name": e.name, "type": e.type, "description": e.description}
                for e in elements
            ],
            "count": len(elements)
        }
    else:
        raise HTTPException(status_code=400, detail=f"Unsupported language: {language}")
