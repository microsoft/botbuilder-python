from ..expression_evaluator import ExpressionEvaluator, EvaluateExpressionDelegate
from ..expression_type import FLOAT
from ..function_utils import FunctionUtils
from ..return_type import ReturnType


class Float(ExpressionEvaluator):
    def __init__(self):
        super().__init__(
            FLOAT, Float.evaluator(), ReturnType.Number, FunctionUtils.validate_unary
        )

    @staticmethod
    def evaluator() -> EvaluateExpressionDelegate:
        def anonymous_function(args: []):
            return float(args[0])

        return FunctionUtils.apply(anonymous_function)
