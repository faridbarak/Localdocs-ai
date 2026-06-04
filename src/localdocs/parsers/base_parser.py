"""Base parser abstraction layer for multiple programming languages"""
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import List


@dataclass
class CodeElement:
    name: str
    type: str
    description: str = ""
    # Standard field factory prevents mutable list reference issues in Python
    parameters: List[str] = field(default_factory=list)
    return_type: str = ""
    line_number: int = 0


class BaseParser(ABC):
    def __init__(self, code: str):
        self.code = code
        self.elements: List[CodeElement] = []
    
    @abstractmethod
    def parse(self) -> List[CodeElement]:
        """Parse raw code string and return extracted abstract components"""
        pass
