from dateutil import tz
from dateutil.parser import parse
from ..time_zone_converter import TimeZoneConverter
from ..options import Options
from ..expression_type import CONVERTTOUTC
from ..function_utils import FunctionUtils
from ..return_type import ReturnType
from ..expression_evaluator import ExpressionEvaluator
from ..convert_format import FormatDatetime


class ConvertToUtc(ExpressionEvaluator):
    def __init__(self):
        super().__init__(
            CONVERTTOUTC,
            ConvertToUtc.evaluator,
            ReturnType.String,
            ConvertToUtc.validator,
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
                value, error = ConvertToUtc.eval_convert_to_utc(
                    args[0], args[1], time_format
                )
            else:
                error = (
                    "{"
                    + expression.to_string()
                    + "} should contain an ISO format timestamp,"
                    + " a origin time zone string and an optional output format string."
                )
        return value, error

    @staticmethod
    def eval_convert_to_utc(src_timestamp: object, timezone: str, time_format: str):
        error: str = None
        result: str = None
        parsed: object = None
        if isinstance(src_timestamp, str):
            try:
                parsed = parse(src_timestamp)
            except:
                error = "illegal time-stamp representation {" + src_timestamp + "}."
        else:
            parsed = src_timestamp
        if error is None:
            source_timezone = TimeZoneConverter.windows_to_lana(timezone)
            if not TimeZoneConverter.verify_time_zone_str(source_timezone):
                error = "{" + source_timezone + "} is an illegal timezone."
            converted_datetime = parsed.replace(tzinfo=tz.gettz(source_timezone))
            if error is None:
                result = FormatDatetime.format(
                    converted_datetime.astimezone(tz.gettz("UTC")), time_format
                )
        return result, error

    @staticmethod
    def validator(expression: object):
        FunctionUtils.validate_arity_and_any_type(expression, 2, 3, ReturnType.String)
