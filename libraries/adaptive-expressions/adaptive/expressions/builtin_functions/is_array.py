from ..expression_evaluator import ExpressionEvaluator, EvaluateExpressionDelegate
from ..expression_type import ISARRAY
from ..function_utils import FunctionUtils
from ..return_type import ReturnType


class IsArray(ExpressionEvaluator):
    def __init__(self):
        super().__init__(
            ISARRAY,
            IsArray.evaluator(),
            ReturnType.Boolean,
            FunctionUtils.validate_unary,
        )

    @staticmethod
    def evaluator() -> EvaluateExpressionDelegate:
        def anonymous_function(args: []):
            return isinstance(args[0], list)

        return FunctionUtils.apply(anonymous_function)
