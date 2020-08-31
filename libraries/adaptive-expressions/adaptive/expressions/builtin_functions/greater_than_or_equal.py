from .comparison_evaluator import ComparisonEvaluator
from ..expression_type import GREATERTHANOREQUAL
from ..function_utils import FunctionUtils


class GreaterThanOrEqual(ComparisonEvaluator):
    def __init__(self):
        super().__init__(
            GREATERTHANOREQUAL,
            GreaterThanOrEqual.function,
            FunctionUtils.validate_binary_number_or_string,
            FunctionUtils.verify_number_or_string,
        )

    @staticmethod
    def function(args: list):
        return float(args[0]) >= float(args[1])
