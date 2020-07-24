import operator
from .comparison_evaluator import ComparisonEvaluator
from ..expression_type import EQUAL
from ..function_utils import FunctionUtils

class Equal(ComparisonEvaluator):
    def __init__(self):
        super().__init__(EQUAL, Equal.function, FunctionUtils.validate_binary)

    @staticmethod
    def function(args: list):
        if args[0] is None or args[1] is None:
            return args[0] is None and args[1] is None
        return operator.eq(args[0], args[1])
