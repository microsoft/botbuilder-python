import re
from datetime import datetime, time
from dateutil import tz
from datatypes_timex_expression import Timex
from ..options import Options
from ..expression_type import GETNEXTVIABLETIME
from ..function_utils import FunctionUtils
from ..return_type import ReturnType
from ..expression_evaluator import ExpressionEvaluator
from ..time_zone_converter import TimeZoneConverter


class GetNextViableTime(ExpressionEvaluator):
    def __init__(self):
        super().__init__(
            GETNEXTVIABLETIME,
            GetNextViableTime.evaluator,
            ReturnType.String,
            FunctionUtils.validate_unary_or_binary_string,
        )

    @staticmethod
    def evaluator(expression: object, state: object, options: Options):
        parsed: object = None
        value: str = None
        error: str = None
        args: list = []
        current_time: datetime = datetime.utcnow()
        valid_hour = 0
        valid_minute = 0
        valid_second = 0
        converted_datetime: object = None
        pattern = re.compile("TXX:[0-5][0-9]:[0-5][0-9]")
        res = FunctionUtils.evaluate_children(expression, state, options)
        args = res[0]
        error = res[1]
        if not error:
            if not pattern.match(args[0]):
                # pylint: disable=line-too-long
                error = "{} must be a timex string which only contains minutes and seconds, for example: 'TXX:15:28'".format(
                    args[0]
                )

        if not error:
            if len(args) == 2 and isinstance(args[1], str):
                time_zone = TimeZoneConverter.windows_to_lana(args[1])
                if not TimeZoneConverter.verify_time_zone_str(time_zone):
                    error = "{} is not a valid timezone".format(args[1])

                if not error:
                    converted_datetime = current_time.astimezone(tz.gettz(time_zone))
            else:
                converted_datetime = current_time

        if not error:
            result = FunctionUtils.parse_timex_property(
                str(args[0]).replace("XX", "00")
            )
            parsed = result[0]
            error = result[1]

        if not error:
            hour = converted_datetime.hour
            minute = converted_datetime.minute
            second = converted_datetime.second

            if parsed.minute > minute or (
                parsed.minute == minute and parsed.second >= second
            ):
                valid_hour = hour
            else:
                valid_hour = hour + 1

            if valid_hour > 24:
                valid_hour -= 24

            valid_minute = parsed.minute
            valid_second = parsed.second

        value = Timex.from_time(
            time(valid_hour, valid_minute, valid_second)
        ).timex_value()

        return value, error
