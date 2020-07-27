from ..expression_evaluator import ExpressionEvaluator
from ..expression_type import LENGTH
from ..function_utils import FunctionUtils
from ..return_type import ReturnType


class Length(ExpressionEvaluator):
    def __init__(self):
        super().__init__(
            LENGTH,
            Length.evaluator(),
            ReturnType.Number,
            FunctionUtils.validate_unary_string,
        )

    @staticmethod
    def evaluator():
        def anonymous_function(args: list):
            result = 0
            if isinstance(args[0], str):
                result = len(str(args[0]))
            else:
                result = 0
            return result

        return FunctionUtils.apply(
            anonymous_function, FunctionUtils.verify_string_or_null
        )
