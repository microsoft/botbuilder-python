from ..expression_evaluator import ExpressionEvaluator, EvaluateExpressionDelegate
from ..expression_type import RANGE
from ..function_utils import FunctionUtils
from ..return_type import ReturnType


class Range(ExpressionEvaluator):
    def __init__(self):
        super().__init__(
            RANGE,
            Range.evaluator(),
            ReturnType.Array,
            FunctionUtils.validate_binary_number,
        )

    @staticmethod
    def evaluator() -> EvaluateExpressionDelegate:
        def anonymous_function(args: []):
            error: str = None
            value: list = None
            result: int = 0
            result, error = FunctionUtils.parse_int(args[1])
            count: int = result
            if error is None:
                if count <= 0:
                    error = (
                        "The second parameter " + args[1] + " should be more than zero"
                    )
                else:
                    result = 0
                    result, error = FunctionUtils.parse_int(args[0])
                    if error is None:
                        value = list(range(result, result + count))

            return value, error

        return FunctionUtils.apply_with_error(
            anonymous_function, FunctionUtils.verify_integer
        )
