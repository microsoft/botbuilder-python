import sys
from ..expression_evaluator import ExpressionEvaluator, EvaluateExpressionDelegate
from ..expression_type import INTERSECTION
from ..function_utils import FunctionUtils
from ..return_type import ReturnType


class Intersection(ExpressionEvaluator):
    def __init__(self):
        super().__init__(
            INTERSECTION,
            Intersection.evaluator(),
            ReturnType.Array,
            Intersection.validator,
        )

    @staticmethod
    def evaluator() -> EvaluateExpressionDelegate:
        def anonymous_function(args: list):
            result = args[0]
            for arg in args:
                result = list(filter(lambda e, argRes=arg: (e in argRes), result))

            return sorted(list(set(result)))

        return FunctionUtils.apply(anonymous_function, FunctionUtils.verify_list)

    @staticmethod
    def validator(expression: object):
        FunctionUtils.validate_arity_and_any_type(
            expression, 1, sys.maxsize, ReturnType.Array
        )
