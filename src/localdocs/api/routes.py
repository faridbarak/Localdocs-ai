"""API routes for LocalDocs AI"""
import os
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
    try:
        return {"models": [settings.default_model], "default": settings.default_model}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/api/v1/generate-docs", response_model=GenerateDocsResponse)
async def generate_docs(request: GenerateDocsRequest):
    """Generate documentation for code and save it physically to disk"""
    try:
        # 1. Parse code architecture
        parser = PythonParser(request.code)
        elements = parser.parse()

        # 2. Generate AI documentation explanation block
        try:
            ai_docs = ollama_client.generate_docs(
                code=request.code,
                model=request.model
            )
        except Exception as ollama_err:
            # Fallback text if Ollama engine is offline or unresponsive
            ai_docs = f"Error: Failed to communicate with local LLM engine. Details: {str(ollama_err)}"

        # 3. Combine parsed formatting + AI generation text blocks
        markdown = MarkdownGenerator.generate(elements, request.project_name)
        markdown += "\n\n## AI-Generated Documentation\n\n"
        markdown += ai_docs

        # 4. Save the Markdown file physically to the storage disk directory
        try:
            os.makedirs(settings.storage_dir, exist_ok=True)
            # Sanitize the project name to create a safe filename
            safe_filename = f"{request.project_name.lower().replace(' ', '_')}_docs.md"
            file_path = os.path.join(settings.storage_dir, safe_filename)
            
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(markdown)
        except Exception as file_err:
            # System logs the file write error but doesn't break the response loop
            print(f"File Storage Warning: Failed to save markdown to disk. Details: {file_err}")

        return GenerateDocsResponse(
            success=True,
            documentation=markdown,
            elements_count=len(elements),
            model_used=request.model or settings.default_model
        )

    except ConnectionError as e:
        raise HTTPException(status_code=503, detail=f"Service unavailable: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal system processing error: {str(e)}")


@router.post("/api/v1/parse-code")
async def parse_code(code: str, language: str = "python"):
    """Parse code structural elements without triggering local LLM generation"""
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
