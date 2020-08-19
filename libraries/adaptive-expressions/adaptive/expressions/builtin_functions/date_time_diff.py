from ..options import Options
from ..expression_type import DATETIMEDIFF
from ..function_utils import FunctionUtils
from ..return_type import ReturnType
from ..expression_evaluator import ExpressionEvaluator


class DateTimeDiff(ExpressionEvaluator):
    def __init__(self):
        super().__init__(
            DATETIMEDIFF,
            DateTimeDiff.evaluator,
            ReturnType.Number,
            DateTimeDiff.validator,
        )

    @staticmethod
    def evaluator(expression: object, state, options: Options):
        date_time_start: object = None
        date_time_end: object = None
        value: object = None
        error: str = None
        args: list
        args, error = FunctionUtils.evaluate_children(expression, state, options)
        if error is None:
            date_time_start, error = FunctionUtils.ticks_with_error(args[0])
            if error is None:
                date_time_end, error = FunctionUtils.ticks_with_error(args[1])
            else:
                error = "{" + expression.to_string() + "} must have two ISO timestamps."
        if error is None:
            value = date_time_start - date_time_end
        return value, error

    @staticmethod
    def validator(expression: object):
        FunctionUtils.validate_arity_and_any_type(expression, 2, 2, ReturnType.String)
