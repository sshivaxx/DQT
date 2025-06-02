from typing import Any

from domain.models.validation_rule import ValidationRule


class TypeMatchRule(ValidationRule):
    def __init__(self, expected_type: type):
        super().__init__(f"Value must be type {expected_type.__name__}")
        self.expected_type = expected_type

    def validate(self, value: Any, context: dict = None) -> bool:
        return isinstance(value, self.expected_type)
