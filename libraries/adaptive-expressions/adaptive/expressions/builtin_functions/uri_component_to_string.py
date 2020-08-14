from urllib import parse
from ..expression_evaluator import ExpressionEvaluator, EvaluateExpressionDelegate
from ..expression_type import URICOMPONENTTOSTRING
from ..function_utils import FunctionUtils
from ..return_type import ReturnType


class UriComponentToString(ExpressionEvaluator):
    def __init__(self):
        super().__init__(
            URICOMPONENTTOSTRING,
            UriComponentToString.evaluator(),
            ReturnType.String,
            FunctionUtils.validate_unary,
        )

    @staticmethod
    def evaluator() -> EvaluateExpressionDelegate:
        def anonymous_function(args: []):
            return parse.unquote_plus(args[0])

        return FunctionUtils.apply(anonymous_function, FunctionUtils.verify_string)
