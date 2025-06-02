from typing import Any, Optional, Dict, List

from pydantic import BaseModel
from datetime import datetime


class ValidationResult(BaseModel):
    is_valid: bool
    value: Any
    error: Optional[str]
    rule_weight: float
    context: Optional[Dict[str, Any]] = None
    timestamp: datetime = datetime.now()


class ValidationReport:
    def __init__(self):
        self.results: List[ValidationResult] = []
        self.metrics: Dict[str, Any] = {}
        self._snapshots: List[dict] = []

    def add_result(self, result: ValidationResult):
        self.results.append(result)

    def take_snapshot(self):
        self._snapshots.append({
            'timestamp': datetime.now(),
            'metrics': self.metrics.copy(),
            'error_stats': self._calculate_error_stats()
        })

    def calculate_metrics(self):
        total_weight = sum(r.rule_weight for r in self.results)
        valid_weight = sum(r.rule_weight for r in self.results if r.is_valid)

        self.metrics = {
            'total_checked': len(self.results),
            'errors_count': len(self.results) - sum(r.is_valid for r in self.results),
            'success_rate': valid_weight / total_weight if total_weight > 0 else 0,
            'weighted_score': valid_weight / total_weight if total_weight > 0 else 0
        }

    def _calculate_error_stats(self) -> dict:
        error_counts = {}
        for result in self.results:
            if not result.is_valid:
                error_counts[result.error] = error_counts.get(result.error, 0) + 1
        return error_counts
