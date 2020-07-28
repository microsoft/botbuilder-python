from ..expression_evaluator import ExpressionEvaluator, EvaluateExpressionDelegate
from ..expression_type import STARTSWITH
from ..function_utils import FunctionUtils
from ..return_type import ReturnType


class StartsWith(ExpressionEvaluator):
    def __init__(self):
        super().__init__(
            STARTSWITH, StartsWith.evaluator(), ReturnType.Boolean, StartsWith.validator
        )

    @staticmethod
    def evaluator() -> EvaluateExpressionDelegate:
        def anonymous_function(args: list):
            raw_str: str = ""
            if isinstance(args[0], str):
                raw_str = args[0]
            seek_str: str = ""
            if isinstance(args[1], str):
                seek_str = args[1]
            return raw_str.startswith(seek_str)
        return FunctionUtils.apply(
            anonymous_function, FunctionUtils.verify_string_or_null
        )

    @staticmethod
    def validator(expression: object):
        FunctionUtils.validate_arity_and_any_type(expression, 2, 2, ReturnType.String)
