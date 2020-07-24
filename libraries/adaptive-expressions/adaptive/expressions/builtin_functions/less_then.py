from .comparison_evaluator import ComparisonEvaluator
from ..expression_type import LESSTHEN
from ..function_utils import FunctionUtils

class LessThen(ComparisonEvaluator):
    def __init__(self):
        super().__init__(
            LESSTHEN,
            LessThen.function,
            FunctionUtils.validate_binary_number_or_string,
            FunctionUtils.verify_number_or_string_or_null,
        )

    @staticmethod
    def function(args: list):
        return float(args[0]) < float(args[1])
