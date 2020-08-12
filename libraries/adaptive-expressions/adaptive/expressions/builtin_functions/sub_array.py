from ..expression_evaluator import ExpressionEvaluator
from ..expression_type import SUBARRAY
from ..function_utils import FunctionUtils
from ..return_type import ReturnType
from ..memory_interface import MemoryInterface
from ..options import Options


class SubArray(ExpressionEvaluator):
    def __init__(self):
        super().__init__(
            SUBARRAY, SubArray.evaluator, ReturnType.Array, SubArray.validator,
        )

    @staticmethod
    def evaluator(expression: object, state: MemoryInterface, options: Options):
        result: object = None
        error: str = None
        arr: list = None
        res = expression.children[0].try_evaluate(state, options)

        arr = res[0]
        error = res[1]

        if error is None:
            if isinstance(arr, list):
                start: int

                start_expr = expression.children[1]
                res = start_expr.try_evaluate(state, options)
                start = res[0]
                error = res[1]
                if error is None and not FunctionUtils.is_integer(start):
                    error = start_expr.to_string() + " is not an integer."
                elif start < 0 or start >= len(arr):
                    error = (
                        start_expr.to_string()
                        + "="
                        + str(start)
                        + " which is out of range for "
                        + str(arr)
                    )

                if error is None:
                    end: int
                    if len(expression.children) == 2:
                        end = len(arr)
                    else:
                        end_expr = expression.children[2]
                        res = end_expr.try_evaluate(state, options)
                        end = res[0]
                        error = res[1]
                        if error is None and not FunctionUtils.is_integer(end):
                            error = end_expr.to_string() + " is not an integer."
                        elif end < 0 or end > len(arr):
                            error = (
                                end_expr.to_string()
                                + "="
                                + str(end)
                                + " which is out of range for "
                                + str(arr)
                            )

                    if error is None:
                        result = arr[int(start) : int(end)]
            else:
                error = expression.children[0].to_string() + "is not array."

        value = result

        return value, error

    @staticmethod
    def validator(expression: object):
        FunctionUtils.validate_order(
            expression, [ReturnType.Number], ReturnType.Array, ReturnType.Number
        )
