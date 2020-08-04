from ..expression_evaluator import ExpressionEvaluator, EvaluateExpressionDelegate
from ..expression_type import ROUND
from ..function_utils import FunctionUtils
from ..return_type import ReturnType


class Round(ExpressionEvaluator):
    def __init__(self):
        super().__init__(
            ROUND,
            Round.evaluator(),
            ReturnType.Number,
            FunctionUtils.validate_unary_or_binary_number,
        )

    @staticmethod
    def evaluator() -> EvaluateExpressionDelegate:
        def anonymous_function(args: []):
            error: str = None
            result: object = None
            if len(args) == 2 and not FunctionUtils.is_integer(args[1]):
                error = "The second " + args[1] + " parameter must be an integer."

            if error is None:
                digits = 0
                if len(args) == 2:
                    result, error = FunctionUtils.parse_int(args[1])
                    digits = result
                    result = None

                if error is None:
                    if digits < 0 or digits > 15:
                        error = (
                            "The second parameter "
                            + args[1]
                            + " must be an integer between 0 and 15"
                        )
                    else:
                        result = round(args[0], digits)

            return result, error

        return FunctionUtils.apply_with_error(
            anonymous_function, FunctionUtils.verify_number
        )
