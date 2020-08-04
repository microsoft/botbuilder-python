from ..expression_evaluator import ExpressionEvaluator, EvaluateExpressionDelegate
from ..expression_type import ISSTRING
from ..function_utils import FunctionUtils
from ..return_type import ReturnType


class IsString(ExpressionEvaluator):
    def __init__(self):
        super().__init__(
            ISSTRING, IsString.evaluator(), ReturnType.Boolean, FunctionUtils.validate_unary
        )

    @staticmethod
    def evaluator() -> EvaluateExpressionDelegate:
        def anonymous_function(args: []):
            return isinstance(args[0], str)

        return FunctionUtils.apply(anonymous_function)
