from abc import ABC, abstractmethod
from typing import Any

class ValidationRule(ABC):
    def __init__(self, error_message: str, weight: float = 1.0):
        self.error_message = error_message
        self.weight = weight

    @abstractmethod
    def validate(self, value: Any, context: dict = None) -> bool:
        pass
