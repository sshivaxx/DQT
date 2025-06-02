from abc import abstractmethod
from typing import Any

from domain.models.validation_rule import ValidationRule


class ContextualRule(ValidationRule):
    def validate(self, value: Any, context: dict = None) -> bool:
        return self._check_context(value, context or {})

    @abstractmethod
    def _check_context(self, value: Any, context: dict) -> bool:
        pass
