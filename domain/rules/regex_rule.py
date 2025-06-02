import re
from domain.models.validation_rule import ValidationRule


class RegexRule(ValidationRule):
    def __init__(self, pattern: str):
        super().__init__(f"Value must match pattern: {pattern}")
        self.pattern = re.compile(pattern)

    def validate(self, value: str, **kwargs) -> bool:
        return bool(self.pattern.match(str(value)))