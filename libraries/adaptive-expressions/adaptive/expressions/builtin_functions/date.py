from datetime import datetime
from ..expression_evaluator import ExpressionEvaluator, EvaluateExpressionDelegate
from ..expression_type import DATE
from ..function_utils import FunctionUtils
from ..return_type import ReturnType

class Date(ExpressionEvaluator):
    def __init__(self):
        super().__init__(
            DATE, Date.evaluator(), ReturnType.String, FunctionUtils.validate_unary
        )

    @staticmethod
    def evaluator() -> EvaluateExpressionDelegate:
        def anonymous_function(args: list):
            def anonymous_func(date_time: datetime):
                result = date_time.strftime("%m/%d/%Y")
                result = result if result[0] != "0" else result[1:]
                return result, None
            return FunctionUtils.normalize_to_date_time(args[0], anonymous_func)
        return FunctionUtils.apply_with_error(anonymous_function)
