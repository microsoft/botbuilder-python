import sys
import jsonmerge
from ..expression_type import MERGE
from ..function_utils import FunctionUtils
from ..return_type import ReturnType
from ..expression_evaluator import ExpressionEvaluator, EvaluateExpressionDelegate


class Merge(ExpressionEvaluator):
    def __init__(self):
        super().__init__(
            MERGE, Merge.evaluator(), ReturnType.Object, Merge.validator,
        )

    @staticmethod
    def evaluator() -> EvaluateExpressionDelegate:
        def anonymous_function(args: list):
            result: object = None
            error: str = None
            try:
                jsonmerge.merge(args[1], args[0])
                result = jsonmerge.merge(args[0], args[1])
            except:
                error = (
                    "The arguments {"
                    + args[0]
                    + "} and {"
                    + args[1]
                    + "} must be a JSON objects."
                )
            return result, error

        return FunctionUtils.apply_sequence_with_error(anonymous_function)

    @staticmethod
    def validator(expression: object):
        FunctionUtils.validate_arity_and_any_type(expression, 2, sys.maxsize)
