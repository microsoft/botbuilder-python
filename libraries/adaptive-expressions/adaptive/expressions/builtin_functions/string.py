from ..expression_evaluator import ExpressionEvaluator, EvaluateExpressionDelegate
from ..expression_type import STRING
from ..function_utils import FunctionUtils
from ..return_type import ReturnType


class String(ExpressionEvaluator):
    def __init__(self):
        super().__init__(
            STRING, String.evaluator(), ReturnType.String, FunctionUtils.validate_unary
        )

    @staticmethod
    def evaluator() -> EvaluateExpressionDelegate:
        def anonymous_function(args: []):
            return str(args[0]).strip('"')

        return FunctionUtils.apply(anonymous_function)
