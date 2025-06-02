from typing import List, Any

from domain.models.validation_rule import ValidationRule


class CompositeRule(ValidationRule):
    def __init__(self, rules: List[ValidationRule], operator: str = 'AND'):
        super().__init__(f"Composite rule ({operator})", weight=sum(r.weight for r in rules))
        self.rules = rules
        self.operator = operator.upper()

    def validate(self, value: Any, context: dict = None) -> bool:
        results = [rule.validate(value, context) for rule in self.rules]
        return self._apply_operator(results)

    def _apply_operator(self, results: List[bool]) -> bool:
        if self.operator == 'AND':
            return all(results)
        if self.operator == 'OR':
            return any(results)
        if self.operator == 'AT_LEAST':
            required = len(self.rules) - 1
            return sum(results) >= required
        raise ValueError(f"Unknown operator: {self.operator}")
