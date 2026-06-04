"""Python code parser using the native Abstract Syntax Tree (AST)"""
import ast
from typing import List, Optional
from localdocs.parsers.base_parser import BaseParser, CodeElement


class PythonParser(BaseParser):
    """Parser designed to break down and extract structural elements from Python code"""

    def parse(self) -> List[CodeElement]:
        try:
            tree = ast.parse(self.code)
            self.elements = []

            # Iterate through the elements at the root level of the module body
            for node in tree.body:
                self._process(node, None)

            return self.elements
        except SyntaxError as e:
            print(f"Syntax error while parsing: {e}")
            return []

    def _process(self, node, parent_prefix: Optional[str] = None):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            elem = self._parse_function(node, parent_prefix)
            self.elements.append(elem)
        elif isinstance(node, ast.ClassDef):
            elem = self._parse_class(node, parent_prefix)
            self.elements.append(elem)
            
            # Dynamically build the nested namespace path
            current_prefix = f"{parent_prefix}.{node.name}" if parent_prefix else node.name
            
            # Recursively walk down child nodes inside the class body
            for child in node.body:
                self._process(child, current_prefix)

    def _parse_function(self, node, parent_prefix: Optional[str]) -> CodeElement:
        params = [arg.arg for arg in node.args.args]
        docstring = ast.get_docstring(node) or ""

        name = f"{parent_prefix}.{node.name}" if parent_prefix else node.name
        first_line_desc = docstring.split("\n")[0] if docstring else ""

        return CodeElement(
            name=name,
            type="method" if parent_prefix else "function",
            description=first_line_desc.strip(),
            parameters=params,
            line_number=node.lineno
        )

    def _parse_class(self, node: ast.ClassDef, parent_prefix: Optional[str] = None) -> CodeElement:
        docstring = ast.get_docstring(node) or ""
        first_line_desc = docstring.split("\n")[0] if docstring else ""
        
        name = f"{parent_prefix}.{node.name}" if parent_prefix else node.name

        return CodeElement(
            name=name,
            type="class",
            description=first_line_desc.strip(),
            line_number=node.lineno
        )
