from ..expression_evaluator import ExpressionEvaluator, EvaluateExpressionDelegate
from ..expression_type import FIRST
from ..function_utils import FunctionUtils
from ..return_type import ReturnType


class First(ExpressionEvaluator):
    def __init__(self):
        super().__init__(
            FIRST, First.evaluator(), ReturnType.Object, FunctionUtils.validate_unary
        )

    @staticmethod
    def evaluator() -> EvaluateExpressionDelegate:
        def anonymous_function(args: []):
            first: object = None
            if isinstance(args[0], str) and len(args[0]) > 0:
                first = args[0][0]

            if isinstance(args[0], list) and len(args[0]) > 0:
                first = FunctionUtils.access_index(args[0], 0)[0]

            return first

        return FunctionUtils.apply(anonymous_function)
