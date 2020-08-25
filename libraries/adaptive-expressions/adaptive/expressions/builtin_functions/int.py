from ..expression_evaluator import ExpressionEvaluator, EvaluateExpressionDelegate
from ..expression_type import INT
from ..function_utils import FunctionUtils
from ..return_type import ReturnType


class Int(ExpressionEvaluator):
    def __init__(self):
        super().__init__(
            INT, Int.evaluator(), ReturnType.Number, FunctionUtils.validate_unary
        )

    @staticmethod
    def evaluator() -> EvaluateExpressionDelegate:
        def anonymous_function(args: []):
            return int(args[0])

        return FunctionUtils.apply(anonymous_function)
