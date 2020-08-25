from ..common_regex import CommonRegex
from ..expression_evaluator import ExpressionEvaluator, EvaluateExpressionDelegate
from ..expression_type import ISMATCH, CONSTANT
from ..function_utils import FunctionUtils
from ..return_type import ReturnType


class IsMatch(ExpressionEvaluator):
    def __init__(self):
        super().__init__(
            ISMATCH, IsMatch.evaluator(), ReturnType.Boolean, IsMatch.validator,
        )

    @staticmethod
    def evaluator() -> EvaluateExpressionDelegate:
        def anonymous_function(args: []):
            value: bool = False
            error: str = None
            input_string = args[0]
            if input_string is None or len(input_string) == 0:
                value = False
                error = "regular expression is empty."
            else:
                regex = CommonRegex.create_regex(args[1])
                value = regex.match(input_string) is not None
            return value, error

        return FunctionUtils.apply_with_error(
            anonymous_function, FunctionUtils.verify_string_or_null
        )

    @staticmethod
    def validator(expression: object):
        FunctionUtils.validate_arity_and_any_type(expression, 2, 2, ReturnType.String)
        second = expression.children[1]
        if second.return_type == ReturnType.String and second.expr_type == CONSTANT:
            CommonRegex.create_regex(second.get_value())
