"""
Python Code Parser
==================
Parses Python code to extract functions, classes, and methods
"""

import ast
from typing import List, Dict, Any


class CodeElement:
    """Represents a parsed code element."""
    
    def __init__(self, name: str, type: str, description: str):
        self.name = name
        self.type = type
        self.description = description
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "type": self.type,
            "description": self.description
        }


class PythonParser:
    """Parser for Python code."""
    
    def __init__(self, code: str):
        self.code = code
        self.elements: List[CodeElement] = []
    
    def parse(self) -> List[CodeElement]:
        """
        Parse Python code and extract elements.
        
        Returns:
            List of CodeElement objects
        """
        try:
            tree = ast.parse(self.code)
            self._extract_elements(tree)
        except SyntaxError as e:
            print(f"Syntax error in code: {e}")
            return []
        
        return self.elements
    
    def _extract_elements(self, tree: ast.AST):
        """Extract all code elements from AST."""
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef) or isinstance(node, ast.AsyncFunctionDef):
                self._add_function(node)
            elif isinstance(node, ast.ClassDef):
                self._add_class(node)
    
    def _add_function(self, node: ast.FunctionDef):
        """Add a function to elements list."""
        description = self._get_docstring(node)
        if not description:
            description = f"Function {node.name}"
        
        element = CodeElement(
            name=node.name,
            type="function",
            description=description
        )
        self.elements.append(element)
    
    def _add_class(self, node: ast.ClassDef):
        """Add a class to elements list."""
        description = self._get_docstring(node)
        if not description:
            description = f"Class {node.name}"
        
        element = CodeElement(
            name=node.name,
            type="class",
            description=description
        )
        self.elements.append(element)
    
    def _get_docstring(self, node: ast.AST) -> str:
        """Get docstring from a node."""
        return ast.get_docstring(node) or ""
