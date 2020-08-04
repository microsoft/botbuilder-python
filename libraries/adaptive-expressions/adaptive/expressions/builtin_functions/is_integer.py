from ..expression_evaluator import ExpressionEvaluator, EvaluateExpressionDelegate
from ..expression_type import ISINTEGER
from ..function_utils import FunctionUtils
from ..return_type import ReturnType


class IsInteger(ExpressionEvaluator):
    def __init__(self):
        super().__init__(
            ISINTEGER, IsInteger.evaluator(), ReturnType.Boolean, FunctionUtils.validate_unary
        )

    @staticmethod
    def evaluator() -> EvaluateExpressionDelegate:
        def anonymous_function(args: []):
            return isinstance(args[0], int)

        return FunctionUtils.apply(anonymous_function)
