from datetime import datetime
from ..options import Options
from ..expression_type import STARTOFHOUR
from ..function_utils import FunctionUtils
from ..return_type import ReturnType
from ..expression_evaluator import ExpressionEvaluator


class StartOfHour(ExpressionEvaluator):
    def __init__(self):
        super().__init__(
            STARTOFHOUR, StartOfHour.evaluator, ReturnType.String, StartOfHour.validator
        )

    @staticmethod
    def evaluator(expression: object, state, options: Options):
        value: object = None
        error: str = None
        args: list
        args, error = FunctionUtils.evaluate_children(expression, state, options)
        if error is None:
            time_format = (
                args[1] if len(args) == 2 else FunctionUtils.default_date_time_format
            )
            value, error = StartOfHour.start_of_hour_with_error(args[0], time_format)
            if len(args) != 2:
                value = value[:-4] + "Z"
        return value, error

    @staticmethod
    def start_of_hour_with_error(timestamp: object, time_format: str):
        result: str = None
        error: str = None
        parsed: object = None
        parsed, error = FunctionUtils.normalize_to_date_time(timestamp)
        if error is None:
            start_of_hour = datetime(
                year=parsed.year, month=parsed.month, day=parsed.day, hour=parsed.hour
            )
            result = start_of_hour.strftime(time_format)
        return result, error

    @staticmethod
    def validator(expression: object):
        FunctionUtils.validate_arity_and_any_type(expression, 1, 2, ReturnType.String)
