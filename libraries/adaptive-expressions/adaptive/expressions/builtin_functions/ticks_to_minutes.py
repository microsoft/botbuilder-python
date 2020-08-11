from ..options import Options
from ..expression_type import TICKSTOMINUTES
from ..function_utils import FunctionUtils
from ..return_type import ReturnType
from ..expression_evaluator import ExpressionEvaluator


class TicksToMinutes(ExpressionEvaluator):
    def __init__(self):
        super().__init__(
            TICKSTOMINUTES,
            TicksToMinutes.evaluator,
            ReturnType.Number,
            FunctionUtils.validate_unary_number,
        )

    ticks_per_minute = 60 * 10000000

    @staticmethod
    def evaluator(expression: object, state, options: Options):
        value: object = None
        error: str = None
        args: list
        args, error = FunctionUtils.evaluate_children(expression, state, options)
        if error is None:
            if isinstance(args[0], int) or (
                isinstance(args[0], float) and args[0].is_integer()
            ):
                value = args[0] / TicksToMinutes.ticks_per_minute
            else:
                error = (
                    "{"
                    + expression.to_string()
                    + "} should contain an integer of ticks."
                )
        return value, error
