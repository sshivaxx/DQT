from domain.models.validation_rule import ValidationRule


class RangeRule(ValidationRule):
    def __init__(self, min_val: float, max_val: float):
        super().__init__(f"Value must be between {min_val} and {max_val}")
        self.min = min_val
        self.max = max_val

    def validate(self, value: float, **kwargs) -> bool:
        return self.min <= value <= self.max

