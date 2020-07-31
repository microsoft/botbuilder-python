from ..expression_evaluator import ExpressionEvaluator, EvaluateExpressionDelegate
from ..expression_type import LAST
from ..function_utils import FunctionUtils
from ..return_type import ReturnType


class Last(ExpressionEvaluator):
    def __init__(self):
        super().__init__(
            LAST, Last.evaluator(), ReturnType.Object, FunctionUtils.validate_unary
        )

    @staticmethod
    def evaluator() -> EvaluateExpressionDelegate:
        def anonymous_function(args: []):
            last: object = None
            if isinstance(args[0], str) and len(args[0]) > 0:
                last = args[0][-1]

            if isinstance(args[0], list) and len(args[0]) > 0:
                last = FunctionUtils.access_index(args[0], len(args[0]) - 1)[0]

            return last

        return FunctionUtils.apply(anonymous_function)
