from ..expression_evaluator import ExpressionEvaluator, EvaluateExpressionDelegate
from ..expression_type import ISBOOLEAN
from ..function_utils import FunctionUtils
from ..return_type import ReturnType


class IsBoolean(ExpressionEvaluator):
    def __init__(self):
        super().__init__(
            ISBOOLEAN, IsBoolean.evaluator(), ReturnType.Boolean, FunctionUtils.validate_unary
        )

    @staticmethod
    def evaluator() -> EvaluateExpressionDelegate:
        def anonymous_function(args: []):
            return type(args[0]) is bool

        return FunctionUtils.apply(anonymous_function)
