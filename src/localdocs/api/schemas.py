"""
API Schemas for LocalDocs AI
============================
Pydantic models for request/response validation
"""

from pydantic import BaseModel
from typing import List, Dict, Any, Optional


class HealthCheckResponse(BaseModel):
    """Health check response schema."""
    message: str
    version: str
    docs: str


class GenerateDocsRequest(BaseModel):
    """Request schema for generating documentation."""
    code: str
    language: Optional[str] = "python"


class CodeElement(BaseModel):
    """Schema for a parsed code element."""
    name: str
    type: str
    description: str


class GenerateDocsResponse(BaseModel):
    """Response schema for generated documentation."""
    success: bool
    documentation: str
    elements_count: int
    elements: List[CodeElement]
