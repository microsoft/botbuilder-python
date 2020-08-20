from ..expression_evaluator import ExpressionEvaluator
from ..expression_type import ISDURATION
from ..function_utils import FunctionUtils
from ..return_type import ReturnType
from ..memory_interface import MemoryInterface
from ..options import Options


class IsDuration(ExpressionEvaluator):
    def __init__(self):
        super().__init__(
            ISDURATION,
            IsDuration.eval,
            ReturnType.String,
            FunctionUtils.validate_unary,
        )

    @staticmethod
    def eval(expression: object, state: MemoryInterface, options: Options):
        parsed: object = None
        value: bool = False
        error: str = None
        args, error = FunctionUtils.evaluate_children(expression, state, options)
        if error is None:
            parsed, error = FunctionUtils.parse_timex_property(args[0])

        if parsed is not None and error is None:
            value = (
                parsed.years is not None
                or parsed.months is not None
                or parsed.weeks is not None
                or parsed.days is not None
                or parsed.hours is not None
                or parsed.minutes is not None
                or parsed.seconds is not None
            )
        return value, error
