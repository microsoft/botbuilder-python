from .comparison_evaluator import ComparisonEvaluator
from ..expression_type import GREATERTHAN
from ..function_utils import FunctionUtils


class GreaterThan(ComparisonEvaluator):
    def __init__(self):
        super().__init__(
            GREATERTHAN,
            GreaterThan.function,
            FunctionUtils.validate_binary_number_or_string,
            FunctionUtils.verify_number_or_string_or_null,
        )

    @staticmethod
    def function(args: list):
        return float(args[0]) > float(args[1])
