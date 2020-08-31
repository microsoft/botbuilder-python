from ..options import Options
from ..expression_type import ADDTOTIME
from ..function_utils import FunctionUtils
from ..return_type import ReturnType
from ..expression_evaluator import ExpressionEvaluator
from ..convert_format import FormatDatetime


class AddToTime(ExpressionEvaluator):
    def __init__(self):
        super().__init__(
            ADDTOTIME, AddToTime.evaluator, ReturnType.String, AddToTime.validator
        )

    @staticmethod
    def evaluator(expression: object, state, options: Options):
        value: object = None
        error: str = None
        args: list
        args, error = FunctionUtils.evaluate_children(expression, state, options)
        if error is None:
            time_format = (
                args[3] if len(args) == 4 else FunctionUtils.default_date_time_format
            )
            if (
                isinstance(args[1], int)
                or (isinstance(args[1], float) and args[1].is_integer())
            ) and isinstance(args[2], str):

                value, error = AddToTime.eval_add_to_time(
                    args[0], args[1], args[2], time_format
                )
            else:
                error = (
                    "{"
                    + expression.to_string()
                    + "} should contain an ISO format timestamp,\
                     a time interval integer, a string unit of time and an optional output format string."
                )
        return value, error

    @staticmethod
    def eval_add_to_time(
        timestamp: object, interval: int, time_unit: str, time_format: str
    ):
        result: str = None
        error: str = None
        parsed: object = None
        parsed, error = FunctionUtils.normalize_to_date_time(timestamp)
        if error is None:
            converter, error = FunctionUtils.date_time_converter(
                interval, time_unit, False
            )
            if error is None:
                added_timestamp = converter(parsed)
                result = FormatDatetime.format(added_timestamp, time_format)
        return result, error

    @staticmethod
    def validator(expression: object):
        FunctionUtils.validate_order(
            expression,
            [ReturnType.String],
            ReturnType.Object,
            ReturnType.Number,
            ReturnType.String,
        )
