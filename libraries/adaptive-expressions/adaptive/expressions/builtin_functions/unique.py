from ..expression_evaluator import ExpressionEvaluator, EvaluateExpressionDelegate
from ..expression_type import UNIQUE
from ..function_utils import FunctionUtils
from ..return_type import ReturnType


class Unique(ExpressionEvaluator):
    def __init__(self):
        super().__init__(UNIQUE, Unique.evaluator(), ReturnType.Array, Unique.validator)

    @staticmethod
    def evaluator() -> EvaluateExpressionDelegate:
        return FunctionUtils.apply(
            lambda args: list(set(args[0])), FunctionUtils.verify_list
        )

    @staticmethod
    def validator(expression: object):
        FunctionUtils.validate_order(expression, None, ReturnType.Array)
