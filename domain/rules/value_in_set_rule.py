from typing import Any

from domain.models.validation_rule import ValidationRule


class ValueInSetRule(ValidationRule):
    def __init__(self, allowed_values: set):
        super().__init__("Value must be in allowed set")
        self.allowed_values = allowed_values

    def validate(self, value: Any, context: dict = None) -> bool:
        return value in self.allowed_values
