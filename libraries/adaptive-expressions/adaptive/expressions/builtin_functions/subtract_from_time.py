from typing import Callable
from datetime import datetime
from ..expression_type import SUBTRACTFROMTIME
from ..function_utils import FunctionUtils
from ..return_type import ReturnType
from ..options import Options
from ..expression_evaluator import ExpressionEvaluator


class SubtractFromTime(ExpressionEvaluator):
    def __init__(self):
        super().__init__(
            SUBTRACTFROMTIME,
            SubtractFromTime.evaluator,
            ReturnType.String,
            SubtractFromTime.validator,
        )

    @staticmethod
    def evaluator(expression: object, state, options: Options):
        value: object = None
        error: str = None
        args: list = []
        args, error = FunctionUtils.evaluate_children(expression, state, options)
        if error is None:
            if (isinstance(args[1], int) or (isinstance(args[1], float) and args[1].is_integer())) and \
                isinstance(args[2], str):

                time_format = (
                    args[3]
                    if len(args) == 4
                    else FunctionUtils.default_date_time_format
                )
                time_converter: Callable[[datetime], datetime]
                time_converter, error = FunctionUtils.date_time_converter(
                    args[1], args[2]
                )
                if error is None:

                    def anonymous_function(date_time: datetime):
                        return (
                            time_converter(date_time).strftime(time_format)[:-4] + "Z",
                            None,
                        )

                    value, error = FunctionUtils.normalize_to_date_time(
                        args[0], anonymous_function
                    )
            else:
                error = (
                    "{"
                    + expression.to_string()
                    + "} should contain an ISO format timestamp,"
                    + "a time interval integer, a string unit of time and an optional output format string."
                )

        return value, error

    @staticmethod
    def validator(expression: object):
        FunctionUtils.validate_order(
            expression,
            [ReturnType.String],
            ReturnType.Object,
            ReturnType.Number,
            ReturnType.String,
        )
