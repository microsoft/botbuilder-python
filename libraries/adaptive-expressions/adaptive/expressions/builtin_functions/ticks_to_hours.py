import numbers
from ..options import Options
from ..expression_type import TICKSTOHOURS
from ..function_utils import FunctionUtils
from ..return_type import ReturnType
from ..expression_evaluator import ExpressionEvaluator


class TicksToHours(ExpressionEvaluator):
    def __init__(self):
        super().__init__(
            TICKSTOHOURS,
            TicksToHours.evaluator,
            ReturnType.Number,
            FunctionUtils.validate_unary_number,
        )

    ticks_per_hour = 60 * 60 * 10000000

    @staticmethod
    def evaluator(expression: object, state, options: Options):
        value: object = None
        error: str = None
        args: list
        args, error = FunctionUtils.evaluate_children(expression, state, options)
        if error is None:
            if isinstance(args[0], numbers.Number):
                value = args[0] / TicksToHours.ticks_per_hour
            else:
                error = (
                    "{"
                    + expression.to_string()
                    + "} should contain an integer of ticks."
                )
        return value, error
