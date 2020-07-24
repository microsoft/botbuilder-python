import numbers
import sys
from ..expression_evaluator import ExpressionEvaluator, EvaluateExpressionDelegate
from ..expression_type import MAX
from ..function_utils import FunctionUtils
from ..return_type import ReturnType


class Max(ExpressionEvaluator):
    def __init__(self):
        super().__init__(
            MAX, Max.evaluator(), ReturnType.Number, FunctionUtils.validate_at_least_one
        )

    @staticmethod
    def evaluator() -> EvaluateExpressionDelegate:
        def anonymous_function(args: []):
            result: object = sys.float_info.min
            if len(args) == 1:
                if isinstance(args[0], list):
                    for value in args[0]:
                        result = Max.eval_max(result, value)
                else:
                    result = Max.eval_max(result, args[0])
            else:
                for arg in args:
                    if isinstance(arg, list):
                        for value in arg:
                            result = Max.eval_max(result, value)
                    else:
                        result = Max.eval_max(result, arg)

            return result

        return FunctionUtils.apply(
            anonymous_function, FunctionUtils.verify_numeric_list_or_number
        )

    @staticmethod
    def eval_max(num_a: numbers.Number, num_b: numbers.Number):
        if num_a is None or num_b is None:
            raise Exception("Argument null exception.")

        return num_a if num_a > num_b else num_b
