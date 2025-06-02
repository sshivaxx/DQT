from concurrent.futures import ThreadPoolExecutor
from functools import lru_cache
from typing import List, Any

from domain.models.data_source import DataSource
from domain.models.validation_report import ValidationResult, ValidationReport
from domain.models.validation_rule import ValidationRule
from domain.rules.cross_column_rule import CrossColumnRule


class ParallelDataValidator:
    def __init__(self, rules: List[ValidationRule], workers: int = 4):
        self.rules = rules
        self.workers = workers
        self.cache_enabled = True

    @lru_cache(maxsize=10_000)
    def _cached_validate(self, rule_idx: int, value: Any) -> bool:
        return self.rules[rule_idx].validate(value)

    def _validate_value(self, value: Any, column: str = None) -> List[ValidationResult]:
        """Валидация отдельного значения всеми правилами"""
        results = []
        for idx, rule in enumerate(self.rules):
            if isinstance(rule, CrossColumnRule):
                continue

            is_valid = self._cached_validate(idx, value)
            results.append(ValidationResult(
                is_valid=is_valid,
                value=value,
                error=None if is_valid else rule.error_message,
                rule_weight=rule.weight,
                context={"column": column} if column else None
            ))
        return results

    def _validate_row(self, row: dict) -> List[ValidationResult]:
        """Обработка целой строки для межколоночных правил"""
        results = []
        for rule in self.rules:
            if isinstance(rule, CrossColumnRule):
                is_valid = rule.validate(row)
                results.append(ValidationResult(
                    is_valid=is_valid,
                    value=row,
                    error=None if is_valid else rule.error_message,
                    rule_weight=rule.weight
                ))
        return results

    def validate_source(self, data_source: DataSource) -> ValidationReport:
        report = ValidationReport()
        data = data_source.read()

        with ThreadPoolExecutor(max_workers=self.workers) as executor:
            if any(isinstance(r, CrossColumnRule) for r in self.rules):
                # Обработка по строкам
                row_results = list(executor.map(self._validate_row, data.to_dict('records')))
                # Обработка по значениям
                col_results = []
                for col in data.columns:
                    col_results.extend(executor.map(
                        lambda v: self._validate_value(v, col),
                        data[col]
                    ))
                results = row_results + col_results
            else:
                # Только обработка по значениям
                results = []
                for col in data.columns:
                    results.extend(executor.map(
                        lambda v: self._validate_value(v, col),
                        data[col]
                    ))

        for result_batch in results:
            report.results.extend(result_batch)

        report.calculate_metrics()
        report.take_snapshot()
        return report
