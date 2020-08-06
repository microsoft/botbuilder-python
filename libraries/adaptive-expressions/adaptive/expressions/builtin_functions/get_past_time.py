import numbers
from datetime import datetime
from ..options import Options
from ..expression_type import GETPASTTIME
from ..function_utils import FunctionUtils
from ..return_type import ReturnType
from ..expression_evaluator import ExpressionEvaluator


class GetPastTime(ExpressionEvaluator):
    def __init__(self):
        super().__init__(
            GETPASTTIME, GetPastTime.evaluator, ReturnType.String, GetPastTime.validator
        )

    @staticmethod
    def evaluator(expression: object, state, options: Options):
        value: object = None
        error: str = None
        args: list = []
        args, error = FunctionUtils.evaluate_children(expression, state, options)
        if error is None:
            if isinstance(args[0], numbers.Number) and isinstance(args[1], str):
                time_format = (
                    args[2]
                    if len(args) == 3
                    else FunctionUtils.default_date_time_format
                )
                time_converter, error = FunctionUtils.date_time_converter(
                    args[0], args[1]
                )
                if error is None:
                    value = time_converter(datetime.utcnow()).strftime(time_format)
                    if len(args) != 3:
                        value = value[:-4] + "Z"
                else:
                    error = (
                        "{"
                        + expression.to_string()
                        + "} should contain a time interval integer"
                        + ", a string unit of time and an optional output format string."
                    )
        return value, error

    @staticmethod
    def validator(expression: object):
        FunctionUtils.validate_order(
            expression, [ReturnType.String], ReturnType.Number, ReturnType.String
        )
