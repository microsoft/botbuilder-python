from datetime import datetime
from dateutil import tz
from datatypes_timex_expression import Timex
from ..options import Options
from ..expression_type import GETNEXTVIABLEDATE
from ..function_utils import FunctionUtils
from ..return_type import ReturnType
from ..expression_evaluator import ExpressionEvaluator
from ..time_zone_converter import TimeZoneConverter


class GetNextViableDate(ExpressionEvaluator):
    def __init__(self):
        super().__init__(
            GETNEXTVIABLEDATE,
            GetNextViableDate.evaluator,
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
        valid_year = 0
        valid_month = 0
        valid_day = 0
        converted_datetime: object = None
        res = FunctionUtils.evaluate_children(expression, state, options)
        args = res[0]
        error = res[1]
        if error is None:
            result = FunctionUtils.parse_timex_property(args[0])
            parsed = result[0]
            error = result[1]

        if parsed and not error:
            if parsed.year or not parsed.month or not parsed.day_of_month:
                # pylint: disable=line-too-long
                error = "{} must be a timex string which only contains month and day-of-month, for example: 'XXXX-10-31'.".format(
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
            year = converted_datetime.year
            month = converted_datetime.month
            day_of_month = converted_datetime.day

            if parsed.month > month or (
                parsed.month == month and parsed.day_of_month >= day_of_month
            ):
                valid_year = year
            else:
                valid_year = year + 1

            valid_month = parsed.month
            valid_day = parsed.day_of_month

            if valid_month == 2 and valid_day == 29:
                while not GetNextViableDate.leap_year(valid_year):
                    valid_year += 1

        value = Timex.from_date(
            datetime(valid_year, valid_month, valid_day)
        ).timex_value()

        return value, error

    @staticmethod
    def leap_year(year: int) -> bool:
        return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)
