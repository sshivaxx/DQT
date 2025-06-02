from typing import List

from domain.models.validation_rule import ValidationRule


class CrossColumnRule(ValidationRule):
    def __init__(self, columns: List[str], check_fn: callable):
        super().__init__(f"Cross-column check for {columns}")
        self.columns = columns
        self.check_fn = check_fn

    def validate(self, row: dict, context: dict = None) -> bool:
        return self.check_fn({col: row[col] for col in self.columns})
