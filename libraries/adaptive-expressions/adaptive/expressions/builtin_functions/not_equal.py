import operator
import numbers
from .comparison_evaluator import ComparisonEvaluator
from ..expression_type import NOTEQUAL
from ..function_utils import FunctionUtils

class NotEqual(ComparisonEvaluator):
    def __init__(self):
        super().__init__(NOTEQUAL, NotEqual.function, FunctionUtils.validate_binary)

    @staticmethod
    def function(args: list):
        if args[0] is None or args[1] is None:
            return not (args[0] is None and args[1] is None)
        if (isinstance(args[0], list) and len(args[0]) == 0) or (isinstance(args[1], list) and len(args[1]) == 0):
            return False
        if (isinstance(args[0], dict) and len(args[0]) == 0) or (isinstance(args[1], dict) and len(args[1]) == 0):
            return False
        if isinstance(args[0], numbers.Number) and isinstance(args[1], numbers.Number):
            if abs(float(args[0]) - float(args[1])) < 0.00000001:
                return False
        return not operator.eq(args[0], args[1])
