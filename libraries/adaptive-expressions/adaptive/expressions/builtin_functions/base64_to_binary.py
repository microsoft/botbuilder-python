import base64
from ..expression_evaluator import ExpressionEvaluator, EvaluateExpressionDelegate
from ..expression_type import BASE64TOBINARY
from ..function_utils import FunctionUtils
from ..return_type import ReturnType


class Base64ToBinary(ExpressionEvaluator):
    def __init__(self):
        super().__init__(
            BASE64TOBINARY,
            Base64ToBinary.evaluator(),
            ReturnType.Object,
            FunctionUtils.validate_unary,
        )

    @staticmethod
    def evaluator() -> EvaluateExpressionDelegate:
        def anonymous_function(args: []):
            return base64.b64decode(str(args[0]))

        return FunctionUtils.apply(anonymous_function, FunctionUtils.verify_string)
