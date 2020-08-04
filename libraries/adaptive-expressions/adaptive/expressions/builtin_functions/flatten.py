import numbers
from functools import reduce
from ..expression_evaluator import ExpressionEvaluator, EvaluateExpressionDelegate
from ..expression_type import FLATTEN
from ..function_utils import FunctionUtils
from ..return_type import ReturnType


class Flatten(ExpressionEvaluator):
    def __init__(self):
        super().__init__(
            FLATTEN, Flatten.evaluator(), ReturnType.Array, Flatten.validator
        )

    @staticmethod
    def evaluator() -> EvaluateExpressionDelegate:
        def anonymous_function(args: []):
            array = args[0]
            depth = int(args[1]) if len(args) > 1 else 100

            return Flatten.eval_flatten(array, depth)

        return FunctionUtils.apply(anonymous_function)

    @staticmethod
    def eval_flatten(arr: list, depth: numbers.Number):
        if not isinstance(depth, numbers.Number) or depth < 1:
            depth = 1

        res = arr
        while depth > 0:
            has_array_item = any(isinstance(x, list) for x in res)
            if has_array_item:
                res = reduce(
                    (
                        lambda x, y: ([x] if not isinstance(x, list) else x)
                        + ([y] if not isinstance(y, list) else y)
                    ),
                    res,
                )
            else:
                break

            depth = depth - 1

        return res

    @staticmethod
    def validator(expression: object):
        FunctionUtils.validate_order(expression, [ReturnType.Number], ReturnType.Array)
