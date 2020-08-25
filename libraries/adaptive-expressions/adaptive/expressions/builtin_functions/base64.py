import base64
from ..expression_evaluator import ExpressionEvaluator, EvaluateExpressionDelegate
from ..expression_type import BASE64
from ..function_utils import FunctionUtils
from ..return_type import ReturnType


class Base64(ExpressionEvaluator):
    def __init__(self):
        super().__init__(
            BASE64, Base64.evaluator(), ReturnType.String, FunctionUtils.validate_unary
        )

    @staticmethod
    def evaluator() -> EvaluateExpressionDelegate:
        def anonymous_function(args: []):
            bytes_string: str = None
            if isinstance(args[0], bytes):
                bytes_string = args[0]
            else:
                bytes_string = str(args[0]).encode(encoding="utf-8")
            return base64.b64encode(bytes_string).decode()

        return FunctionUtils.apply(anonymous_function)
