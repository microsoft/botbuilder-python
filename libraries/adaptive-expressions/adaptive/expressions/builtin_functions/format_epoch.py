from datetime import datetime, timedelta
import numbers
import pytz
from ..expression_evaluator import ExpressionEvaluator, EvaluateExpressionDelegate
from ..expression_type import FORMATEPOCH
from ..function_utils import FunctionUtils
from ..return_type import ReturnType


class FormatEpoch(ExpressionEvaluator):
    def __init__(self):
        super().__init__(
            FORMATEPOCH,
            FormatEpoch.evaluator(),
            ReturnType.String,
            FormatEpoch.validator,
        )

    @staticmethod
    def evaluator() -> EvaluateExpressionDelegate:
        def anonymous_function(args: list):
            result: object = None
            error: str = None
            timestamp = args[0]
            if isinstance(timestamp, numbers.Number):
                date_time = datetime(1970, 1, 1, 0, 0, 0, 0, pytz.timezone("UTC"))
                date_time = date_time + timedelta(seconds=timestamp)
                if len(args) == 2:
                    result = date_time.strftime(args[1])
                else:
                    result = (
                        date_time.strftime(FunctionUtils.default_date_time_format)[:-4]
                        + "Z"
                    )
            else:
                error = (
                    "formatEpoch first argument {"
                    + str(timestamp)
                    + "} is not a number"
                )
            return result, error

        return FunctionUtils.apply_with_error(anonymous_function)

    @staticmethod
    def validator(expression: object):
        FunctionUtils.validate_order(expression, [ReturnType.String], ReturnType.Number)
