from ..options import Options
from ..expression_type import TICKSTODAYS
from ..function_utils import FunctionUtils
from ..return_type import ReturnType
from ..expression_evaluator import ExpressionEvaluator


class TicksToDays(ExpressionEvaluator):
    def __init__(self):
        super().__init__(
            TICKSTODAYS,
            TicksToDays.evaluator,
            ReturnType.Number,
            FunctionUtils.validate_unary_number,
        )

    ticks_per_day = 24 * 60 * 60 * 10000000

    @staticmethod
    def evaluator(expression: object, state, options: Options):
        value: object = None
        error: str = None
        args: list
        args, error = FunctionUtils.evaluate_children(expression, state, options)
        if error is None:
            if isinstance(args[0], int) or (isinstance(args[0], float) and args[0].is_integer()):
                value = args[0] / TicksToDays.ticks_per_day
            else:
                error = (
                    "{"
                    + expression.to_string()
                    + "} should contain an integer of ticks."
                )
        return value, error
