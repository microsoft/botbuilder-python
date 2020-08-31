from datetime import datetime
from dateutil import tz
from ..time_zone_converter import TimeZoneConverter
from ..options import Options
from ..expression_type import CONVERTFROMUTC
from ..function_utils import FunctionUtils
from ..return_type import ReturnType
from ..expression_evaluator import ExpressionEvaluator
from ..convert_format import FormatDatetime


class ConvertFromUtc(ExpressionEvaluator):
    def __init__(self):
        super().__init__(
            CONVERTFROMUTC,
            ConvertFromUtc.evaluator,
            ReturnType.String,
            ConvertFromUtc.validator,
        )

    @staticmethod
    def evaluator(expression: object, state, options: Options):
        value: object = None
        error: str = None
        args: list = []
        args, error = FunctionUtils.evaluate_children(expression, state, options)
        if error is None:
            time_format = (
                args[2] if len(args) == 3 else FunctionUtils.default_date_time_format
            )
            if isinstance(args[1], str):
                value, error = ConvertFromUtc.eval_convert_from_utc(
                    args[0], args[1], time_format
                )
            else:
                error = (
                    "{"
                    + expression.to_string()
                    + "} should contain an ISO format timestamp,"
                    + " a destination time zone string and an optional output format string."
                )
        return value, error

    @staticmethod
    def eval_convert_from_utc(utc_timestamp: object, timezone: str, time_format: str):
        error: str = None
        result: str = None
        utc_datetime = datetime.utcnow()
        parsed: object = None
        parsed, error = FunctionUtils.normalize_to_date_time(utc_timestamp)
        if error is None:
            utc_datetime = parsed.replace(tzinfo=tz.gettz("UTC"))
        if error is None:
            des_timezone = TimeZoneConverter.windows_to_lana(timezone)
            if not TimeZoneConverter.verify_time_zone_str(des_timezone):
                error = "{" + des_timezone + "} is an illegal timezone."
            else:
                result = FormatDatetime.format(
                    utc_datetime.astimezone(tz.gettz(des_timezone)), time_format
                )
        return result, error

    @staticmethod
    def validator(expression: object):
        FunctionUtils.validate_arity_and_any_type(expression, 2, 3, ReturnType.String)
