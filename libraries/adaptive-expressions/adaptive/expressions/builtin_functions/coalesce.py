from ..expression_type import COALESCE
from ..function_utils import FunctionUtils
from ..return_type import ReturnType
from ..expression_evaluator import ExpressionEvaluator, EvaluateExpressionDelegate


class Coalesce(ExpressionEvaluator):
    def __init__(self):
        super().__init__(
            COALESCE,
            Coalesce.evaluator(),
            ReturnType.Object,
            FunctionUtils.validate_at_least_one,
        )

    @staticmethod
    def evaluator() -> EvaluateExpressionDelegate:
        def anonymous_function(args: list):
            return Coalesce.eval_coalesce(args)

        return FunctionUtils.apply(anonymous_function)

    @staticmethod
    def eval_coalesce(object_list: list):
        for obj in object_list:
            if obj is not None:
                return obj
        return None
