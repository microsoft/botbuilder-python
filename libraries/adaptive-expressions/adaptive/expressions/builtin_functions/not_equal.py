from .comparison_evaluator import ComparisonEvaluator
from ..expression_type import NOTEQUAL
from ..function_utils import FunctionUtils


class NotEqual(ComparisonEvaluator):
    def __init__(self):
        super().__init__(NOTEQUAL, NotEqual.function, FunctionUtils.validate_binary)

    @staticmethod
    def function(args: list):
        return not FunctionUtils.is_equal(args)
