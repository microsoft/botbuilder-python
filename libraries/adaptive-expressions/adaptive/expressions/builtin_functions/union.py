import sys
from ..expression_evaluator import ExpressionEvaluator, EvaluateExpressionDelegate
from ..expression_type import UNION
from ..function_utils import FunctionUtils
from ..return_type import ReturnType


class Union(ExpressionEvaluator):
    def __init__(self):
        super().__init__(
            UNION, Union.evaluator(), ReturnType.Array, Union.validator,
        )

    @staticmethod
    def evaluator() -> EvaluateExpressionDelegate:
        def anonymous_function(args: list):
            result = []
            for arg in args:
                result = result + arg

            return sorted(list(set(result)))

        return FunctionUtils.apply(anonymous_function, FunctionUtils.verify_list)

    @staticmethod
    def validator(expression: object):
        FunctionUtils.validate_arity_and_any_type(
            expression, 1, sys.maxsize, ReturnType.Array
        )
