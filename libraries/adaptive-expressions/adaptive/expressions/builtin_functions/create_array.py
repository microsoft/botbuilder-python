from ..expression_evaluator import ExpressionEvaluator, EvaluateExpressionDelegate
from ..expression_type import CREATEARRAY
from ..function_utils import FunctionUtils
from ..return_type import ReturnType


class CreateArray(ExpressionEvaluator):
    def __init__(self):
        super().__init__(CREATEARRAY, CreateArray.evaluator(), ReturnType.Array)

    @staticmethod
    def evaluator() -> EvaluateExpressionDelegate:
        return FunctionUtils.apply(lambda args: args)
