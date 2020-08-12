from ..expression_evaluator import ExpressionEvaluator, EvaluateExpressionDelegate
from ..expression_type import ISFLOAT
from ..function_utils import FunctionUtils
from ..return_type import ReturnType


class IsFloat(ExpressionEvaluator):
    def __init__(self):
        super().__init__(
            ISFLOAT,
            IsFloat.evaluator(),
            ReturnType.Boolean,
            FunctionUtils.validate_unary,
        )

    @staticmethod
    def evaluator() -> EvaluateExpressionDelegate:
        def anonymous_function(args: []):
            return isinstance(args[0], float)

        return FunctionUtils.apply(anonymous_function)
