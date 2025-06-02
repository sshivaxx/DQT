from domain.models.validation_report import ValidationReport, ValidationResult
from domain.models.data_source import DataSource
from domain.models.validation_rule import ValidationRule


class DataValidator:
    def __init__(self, rules: list[ValidationRule]):
        self.rules = rules

    def validate_source(self, data_source: DataSource) -> ValidationReport:
        report = ValidationReport()
        data = data_source.read()

        for column in data.columns:
            for value in data[column]:
                for rule in self.rules:
                    result = ValidationResult(
                        is_valid=rule.validate(value),
                        value=value,
                        error=None if rule.validate(value) else rule.error_message
                    )
                    report.add_result(result)

        report.calculate_metrics()
        return report
