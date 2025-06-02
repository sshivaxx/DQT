from typing import Any

from domain.models.validation_report import ValidationResult
from domain.models.validation_rule import ValidationRule
from domain.models.data_source import DataSource
from domain.services.parallel_data_validator_service import ParallelDataValidator
from domain.exceptions import DomainException
import pandas as pd


class AgeRule(ValidationRule):
    def __init__(self):
        super().__init__(
            error_message="Age must be between 18-99",
            weight=2.0
        )
        self.target_column = "age"

    def validate(self, value: Any, context=None) -> bool:
        try:
            numeric_value = float(value)
            return 18 <= numeric_value <= 99
        except (ValueError, TypeError):
            return False


class EmailRule(ValidationRule):
    def __init__(self):
        super().__init__(
            error_message="Invalid email format",
            weight=1.5
        )
        self.target_column = "email"

    def validate(self, value: Any, context=None) -> bool:
        str_value = str(value)
        return '@' in str_value and '.' in str_value.split('@')[-1]


class SampleDataSource(DataSource):
    def read(self) -> pd.DataFrame:
        return pd.DataFrame({
            'age': [25, "17", "100", "thirty"],
            'email': ['valid@ex.com', 12345, 'good@test.ru', 'bad@com']
        })


# Модифицированный валидатор
class ColumnAwareValidator(ParallelDataValidator):
    def _validate_value(self, value: Any, column: str) -> list:
        """Применяем правила только для целевой колонки"""
        results = []
        for rule in self.rules:
            if rule.target_column != column:
                continue  # Пропускаем правила для других колонок

            is_valid = rule.validate(value)
            results.append(ValidationResult(
                is_valid=is_valid,
                value=value,
                error=None if is_valid else rule.error_message,
                rule_weight=rule.weight,
                context={"column": column}
            ))
        return results


try:
    validator = ColumnAwareValidator(rules=[AgeRule(), EmailRule()])
    report = validator.validate_source(SampleDataSource())

    print(f"Total errors: {report.metrics['errors_count']}")
    for error in report.results:
        if not error.is_valid:
            print(f"Column '{error.context['column']}': {error.value} => {error.error}")

except DomainException as e:
    print(f"Error: {e.message}")