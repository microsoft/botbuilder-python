from ..expression_evaluator import ExpressionEvaluator, EvaluateExpressionDelegate
from ..expression_type import BASE64
from ..function_utils import FunctionUtils
from ..return_type import ReturnType
import base64


class Base64(ExpressionEvaluator):
    def __init__(self):
        super().__init__(
            BASE64, Base64.evaluator(), ReturnType.String, FunctionUtils.validate_unary
        )

    @staticmethod
    def evaluator() -> EvaluateExpressionDelegate:
        def anonymous_function(args: []):
            bytesString: str = None
            if isinstance(args[0], bytes):
                bytesString = args[0]
            else:
                bytesString = str(args[0]).encode(encoding="utf-8")
            return base64.b64encode(bytesString).decode()

        return FunctionUtils.apply(anonymous_function)
