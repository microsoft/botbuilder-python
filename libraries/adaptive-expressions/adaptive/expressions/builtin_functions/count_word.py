import re
from ..expression_evaluator import ExpressionEvaluator, EvaluateExpressionDelegate
from ..expression_type import COUNTWORD
from ..function_utils import FunctionUtils
from ..return_type import ReturnType


class CountWord(ExpressionEvaluator):
    def __init__(self):
        super().__init__(
            COUNTWORD,
            CountWord.evaluator(),
            ReturnType.Boolean,
            FunctionUtils.validate_unary_string,
        )

    @staticmethod
    def evaluator() -> EvaluateExpressionDelegate:
        def anonymous_function(args: list):
            if isinstance(args[0], str):
                return len(re.split(r"\s{1,}", str(args[0]).strip()))
            return 0

        return FunctionUtils.apply(
            anonymous_function, FunctionUtils.verify_string_or_null
        )
