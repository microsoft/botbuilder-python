from ..expression_evaluator import ExpressionEvaluator, EvaluateExpressionDelegate
from ..expression_type import ISOBJECT
from ..function_utils import FunctionUtils
from ..return_type import ReturnType


class IsObject(ExpressionEvaluator):
    def __init__(self):
        super().__init__(
            ISOBJECT,
            IsObject.evaluator(),
            ReturnType.Boolean,
            FunctionUtils.validate_unary,
        )

    @staticmethod
    def evaluator() -> EvaluateExpressionDelegate:
        def anonymous_function(args: []):
            return isinstance(args[0], dict)

        return FunctionUtils.apply(anonymous_function)
