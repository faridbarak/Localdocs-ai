"""JavaScript/TypeScript code parser using regex (no AST dependency)"""
import re
from typing import List
from localdocs.parsers.base_parser import BaseParser, CodeElement


class JavaScriptParser(BaseParser):
    """Parser for JavaScript/TypeScript code structures"""
    
    def parse(self) -> List[CodeElement]:
        """Parse JavaScript code and extract functions, classes, and methods"""
        self.elements = []
        
        if not hasattr(self, 'code') or not self.code:
            if hasattr(self, 'content') and self.content:
                self.code = self.content
            else:
                return []
                
        # Run your extraction loops sequentially
        self._parse_arrow_functions()
        self._parse_regular_functions()
        self._parse_classes()
        self._parse_async_functions()
        
        return self.elements
    
    def _parse_arrow_functions(self):
        """Parse arrow functions"""
        pattern = r'(?:const|let|var)\s+(\w+)\s*=\s*(?:async\s*)?\(([^)]*)\)\s*=>'
        
        for match in re.finditer(pattern, self.code):
            name = match.group(1)
            params_str = match.group(2)
            params = [p.strip().split(':')[0].split('=')[0].strip() 
                     for p in params_str.split(',') if p.strip()]
            
            line_num = self.code[:match.start()].count('\n') + 1
            
            element = CodeElement(
                name=name,
                type="function",
                line_number=line_num,
                description=f"Arrow function with {len(params)} parameter(s)",
                parameters=params
            )
            self.elements.append(element)
    
    def _parse_regular_functions(self):
        """Parse regular function declarations"""
        pattern = r'function\s+(\w+)\s*\(([^)]*)\)'
        
        for match in re.finditer(pattern, self.code):
            name = match.group(1)
            params_str = match.group(2)
            params = [p.strip().split('=')[0].strip() 
                     for p in params_str.split(',') if p.strip()]
            
            line_num = self.code[:match.start()].count('\n') + 1
            
            if any(e.name == name and e.type == "function" for e in self.elements):
                continue
            
            element = CodeElement(
                name=name,
                type="function",
                line_number=line_num,
                description=f"Regular function with {len(params)} parameter(s)",
                parameters=params
            )
            self.elements.append(element)
    
    def _parse_classes(self):
        """Parse class declarations"""
        pattern = r'class\s+(\w+)(?:\s+extends\s+(\w+))?\s*\{'
        
        for match in re.finditer(pattern, self.code):
            name = match.group(1)
            parent = match.group(2) or ""
            
            line_num = self.code[:match.start()].count('\n') + 1
            
            element = CodeElement(
                name=name,
                type="class",
                line_number=line_num,
                description=f"Class{f' extends {parent}' if parent else ''}",
                parameters=[parent] if parent else []
            )
            self.elements.append(element)
            
            # Parse methods nested inside this container body scope
            self._parse_class_methods(name)
    
    def _parse_class_methods(self, class_name: str):
        """Parse methods inside a class block layout"""
        class_pattern = rf'class\s+{class_name}\s*\{{([^}}]*)\}}'
        class_match = re.search(class_pattern, self.code, re.DOTALL)
        
        if not class_match:
            return
        
        class_body = class_match.group(1)
        method_pattern = r'(\w+)\s*\(([^)]*)\)\s*\{'
        
        for match in re.finditer(method_pattern, class_body):
            method_name = match.group(1)
            params_str = match.group(2)
            
            if method_name in ['if', 'for', 'while', 'switch', 'constructor', 'return', 'catch']:
                continue
            
            params = [p.strip().split('=')[0].strip() 
                     for p in params_str.split(',') if p.strip()]
            
            line_num = self.code[:class_match.start() + match.start()].count('\n') + 1
            
            element = CodeElement(
                name=f"{class_name}.{method_name}",
                type="method",
                line_number=line_num,
                description=f"Method with {len(params)} parameter(s)",
                parameters=params
            )
            self.elements.append(element)
    
    def _parse_async_functions(self):
        """Parse async functions"""
        pattern = r'async\s+function\s+(\w+)\s*\(([^)]*)\)'
        
        for match in re.finditer(pattern, self.code):
            name = match.group(1)
            params_str = match.group(2)
            params = [p.strip().split('=')[0].strip() 
                     for p in params_str.split(',') if p.strip()]
            
            line_num = self.code[:match.start()].count('\n') + 1
            
            if any(e.name == name for e in self.elements):
                continue
            
            element = CodeElement(
                name=name,
                type="function",
                line_number=line_num,
                description=f"Async function with {len(params)} parameter(s)",
                parameters=params
            )
            self.elements.append(element)
