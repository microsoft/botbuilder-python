from datatypes_timex_expression import Timex, TimexRelativeConvert, datetime
from ..expression_type import DATEREADBACK
from ..function_utils import FunctionUtils
from ..return_type import ReturnType
from ..expression_evaluator import ExpressionEvaluator


class DateReadBack(ExpressionEvaluator):
    def __init__(self):
        super().__init__(
            DATEREADBACK,
            DateReadBack.evaluator(),
            ReturnType.String,
            DateReadBack.validator,
        )

    @staticmethod
    def evaluator():
        def anonymous_function(args: list):
            result: object = None
            error: str = None
            result, error = FunctionUtils.normalize_to_date_time(args[0])
            if error is None:
                timestamp1 = datetime(result.year, result.month, result.day)
                result, error = FunctionUtils.normalize_to_date_time(args[1])
                if error is None:
                    timestamp2 = result
                    timex = Timex(timex=timestamp2.strftime("%Y-%m-%d"))
                    result = TimexRelativeConvert.convert_timex_to_string_relative(
                        timex, timestamp1
                    )
            return result, error

        return FunctionUtils.apply_with_error(anonymous_function)

    @staticmethod
    def validator(expression: object):
        FunctionUtils.validate_order(
            expression, None, ReturnType.String, ReturnType.String
        )
