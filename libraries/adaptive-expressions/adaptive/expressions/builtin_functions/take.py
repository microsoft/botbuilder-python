from ..expression_evaluator import ExpressionEvaluator
from ..expression_type import TAKE
from ..function_utils import FunctionUtils
from ..return_type import ReturnType
from ..memory_interface import MemoryInterface
from ..options import Options


class Take(ExpressionEvaluator):
    def __init__(self):
        super().__init__(
            TAKE, Take.evaluator, ReturnType.Array, Take.validator,
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
            if isinstance(arr, (list, str)):
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
                    result = arr[0 : int(start)]
            else:
                error = expression.children[0].to_string() + "is not array or string."

        value = result

        return value, error

    @staticmethod
    def validator(expression: object):
        FunctionUtils.validate_order(
            expression, [], ReturnType.Array, ReturnType.Number
        )
