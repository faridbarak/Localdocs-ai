"""Factory selector architecture for dynamic multi-language parsing engine configurations"""
from pathlib import Path
from localdocs.parsers.python_parser import PythonParser
from localdocs.parsers.js_parser import JSParser
from localdocs.parsers.base_parser import BaseParser

class ParserFactory:
    @staticmethod
    def get_parser(file_path: Path, code_content: str) -> BaseParser:
        """Analyze file extensions dynamically and allocate the correct system code parser class"""
        extension = file_path.suffix.lower()
        
        if extension == ".py":
            return PythonParser(code_content)
        elif extension in (".js", ".jsx", ".ts", ".tsx"):
            return JSParser(code_content)
        else:
            raise ValueError(f"Unsupported software engineering language mapping classification extension: {extension}")
