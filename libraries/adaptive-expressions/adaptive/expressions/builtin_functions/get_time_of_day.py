from ..expression_type import GETTIMEOFDAY
from ..function_utils import FunctionUtils
from ..return_type import ReturnType
from ..expression_evaluator import ExpressionEvaluator, EvaluateExpressionDelegate

class GetTimeOfDay(ExpressionEvaluator):
    def __init__(self):
        super().__init__(
            GETTIMEOFDAY, GetTimeOfDay.evaluator(), ReturnType.String, FunctionUtils.validate_unary
        )

    @staticmethod
    def evaluator() -> EvaluateExpressionDelegate:
        def anonymous_function(args: list):
            value: object = None
            error: str = None
            value, error = FunctionUtils.normalize_to_date_time(args[0])
            if error is None:
                timestamp = value
                if timestamp.hour == 0 and timestamp.minute == 0:
                    value = "midnight"
                elif timestamp.hour >= 0 and timestamp.hour < 12:
                    value = "morning"
                elif timestamp.hour == 12 and timestamp.minute == 0:
                    value = "noon"
                elif timestamp.hour < 18:
                    value = "afternoon"
                elif timestamp.hour < 22 or (timestamp.hour == 22 and timestamp.minute == 0):
                    value = "evening"
                else:
                    value = "night"
            return value, error
        return FunctionUtils.apply_with_error(anonymous_function)
