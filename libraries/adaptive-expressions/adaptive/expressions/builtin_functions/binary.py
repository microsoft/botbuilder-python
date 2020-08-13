from ..expression_evaluator import ExpressionEvaluator, EvaluateExpressionDelegate
from ..expression_type import BINARY
from ..function_utils import FunctionUtils
from ..return_type import ReturnType


class Binary(ExpressionEvaluator):
    def __init__(self):
        super().__init__(
            BINARY, Binary.evaluator(), ReturnType.Boolean, FunctionUtils.validate_unary
        )

    @staticmethod
    def evaluator() -> EvaluateExpressionDelegate:
        def anonymous_function(args: []):
            return bytes(args[0], encoding='UTF-8')

        return FunctionUtils.apply(anonymous_function)
