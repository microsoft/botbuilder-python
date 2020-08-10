from ..expression_evaluator import ExpressionEvaluator, EvaluateExpressionDelegate
from ..expression_type import ISDATETIME
from ..function_utils import FunctionUtils
from ..return_type import ReturnType


class IsDateTime(ExpressionEvaluator):
    def __init__(self):
        super().__init__(
            ISDATETIME,
            IsDateTime.evaluator(),
            ReturnType.Boolean,
            FunctionUtils.validate_unary,
        )

    @staticmethod
    def evaluator() -> EvaluateExpressionDelegate:
        def anonymous_function(args: []):
            _, error = FunctionUtils.normalize_to_date_time(args[0])
            if error is None:
                return True
            return False

        return FunctionUtils.apply(anonymous_function)
