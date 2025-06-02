class DomainException(Exception):
    """Базовое исключение доменного слоя"""

    def __init__(self, message: str, code: str = "DOMAIN_ERROR"):
        self.code = code
        self.message = message
        super().__init__(message)


class ValidationError(DomainException):
    """Общее исключение для ошибок валидации"""

    def __init__(self, message: str):
        super().__init__(message, code="VALIDATION_ERROR")


class DataSourceError(DomainException):
    """Ошибки работы с источниками данных"""

    def __init__(self, message: str):
        super().__init__(message, code="DATA_SOURCE_ERROR")


class RuleConfigurationError(DomainException):
    """Ошибки конфигурации правил"""

    def __init__(self, message: str):
        super().__init__(message, code="RULE_CONFIG_ERROR")


class ContextValidationError(ValidationError):
    """Ошибки контекстно-зависимой валидации"""

    def __init__(self, missing_field: str):
        super().__init__(
            f"Missing required context field: {missing_field}"
        )


class CrossColumnValidationError(ValidationError):
    """Ошибки межколоночной валидации"""

    def __init__(self, columns: list):
        super().__init__(
            f"Missing columns for cross-validation: {columns}"
        )


class HistoryException(DomainException):
    """Ошибки работы с историей изменений"""

    def __init__(self, message: str):
        super().__init__(message, code="HISTORY_ERROR")
