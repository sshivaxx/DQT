from typing import Any

from domain.models.validation_rule import ValidationRule


class UniqueValuesRule(ValidationRule):
    def __init__(self):
        super().__init__("Values must be unique", weight=2.0)
        self._seen = set()

    def validate(self, value: Any, context: dict = None) -> bool:
        if value in self._seen:
            return False
        self._seen.add(value)
        return True
