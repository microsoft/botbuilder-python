from .comparison_evaluator import ComparisonEvaluator
from ..expression_type import LESSTHANOREQUAL
from ..function_utils import FunctionUtils


class LessThanOrEqual(ComparisonEvaluator):
    def __init__(self):
        super().__init__(
            LESSTHANOREQUAL,
            LessThanOrEqual.function,
            FunctionUtils.validate_binary_number_or_string,
            FunctionUtils.verify_number_or_string_or_null,
        )

    @staticmethod
    def function(args: list):
        return float(args[0]) <= float(args[1])
