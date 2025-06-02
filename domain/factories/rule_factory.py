from domain.exceptions import ValidationError
from domain.models.validation_rule import ValidationRule
from domain.rules.composite_rule import CompositeRule
from domain.rules.cross_column_rule import CrossColumnRule
from domain.rules.range_rule import RangeRule
from domain.rules.regex_rule import RegexRule
from domain.rules.type_match_rule import TypeMatchRule
from domain.rules.unique_values_rule import UniqueValuesRule
from domain.rules.value_in_set_rule import ValueInSetRule


class RuleFactory:
    @classmethod
    def from_config(cls, config: dict) -> ValidationRule:
        rule_type = config['type']

        mapping = {
            'range': RangeRule,
            'regex': RegexRule,
            'composite': CompositeRule,
            'unique': UniqueValuesRule,
            'type': TypeMatchRule,
            'valueset': ValueInSetRule,
            'cross_column': CrossColumnRule
        }

        if rule_type not in mapping:
            raise ValidationError(f"Unknown rule type: {rule_type}")

        return mapping[rule_type](**config['params'])