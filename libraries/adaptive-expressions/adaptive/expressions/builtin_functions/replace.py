from ..expression_evaluator import ExpressionEvaluator
from ..expression_type import REPLACE
from ..function_utils import FunctionUtils
from ..return_type import ReturnType


class Replace(ExpressionEvaluator):
    def __init__(self):
        super().__init__(
            REPLACE, Replace.evaluator(), ReturnType.String, Replace.validator
        )

    @staticmethod
    def evaluator():
        def anonymous_function(args: list):
            error: str = None
            result: str = None
            input_str: str = ""
            if isinstance(args[0], str):
                input_str = args[0]
            old_str: str = ""
            if isinstance(args[1], str):
                old_str = args[1]
            if len(old_str) == 0:
                error = (
                    "{"
                    + args[1]
                    + "} the oldValue in replace function should be a string with at least length 1."
                )
            new_str: str = ""
            if isinstance(args[2], str):
                new_str = args[2]
            if error is None:
                result = input_str.replace(old_str, new_str)
            return result, error

        return FunctionUtils.apply_with_error(
            anonymous_function, FunctionUtils.verify_string_or_null
        )

    @staticmethod
    def validator(expression: object):
        FunctionUtils.validate_arity_and_any_type(expression, 3, 3, ReturnType.String)
