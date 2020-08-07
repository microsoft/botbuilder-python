from datetime import datetime
from dateutil import tz
from ..expression_evaluator import ExpressionEvaluator, EvaluateExpressionDelegate
from ..expression_type import FORMATTICKS
from ..function_utils import FunctionUtils
from ..return_type import ReturnType


class FormatTicks(ExpressionEvaluator):
    def __init__(self):
        super().__init__(
            FORMATTICKS,
            FormatTicks.evaluator(),
            ReturnType.String,
            FormatTicks.validator,
        )

    @staticmethod
    def evaluator() -> EvaluateExpressionDelegate:
        def anonymous_function(args: list):
            result: object = None
            error: str = None
            timestamp = args[0]
            if isinstance(timestamp, int):
                date_time = datetime.fromtimestamp(
                    # (timestamp - 621356256000000000) / 10000000
                    (timestamp - 621355968000000000) / 10000000
                ).astimezone(tz.gettz("UTC"))
                if len(args) == 2:
                    result = date_time.strftime(args[1])
                else:
                    result = (
                        date_time.strftime(FunctionUtils.default_date_time_format)[:-4]
                        + "Z"
                    )
            else:
                error = (
                    "formatTicks first argument {"
                    + str(timestamp)
                    + "} is not a number"
                )
            return result, error

        return FunctionUtils.apply_with_error(anonymous_function)

    @staticmethod
    def validator(expression: object):
        FunctionUtils.validate_order(expression, [ReturnType.String], ReturnType.Number)
