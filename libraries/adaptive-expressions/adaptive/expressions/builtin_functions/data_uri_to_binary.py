from ..expression_evaluator import ExpressionEvaluator, EvaluateExpressionDelegate
from ..expression_type import DATAURITOBINARY
from ..function_utils import FunctionUtils
from ..return_type import ReturnType
import base64


class DataUriToBinary(ExpressionEvaluator):
    def __init__(self):
        super().__init__(
            DATAURITOBINARY, DataUriToBinary.evaluator(), ReturnType.Object, FunctionUtils.validate_unary
        )

    @staticmethod
    def evaluator() -> EvaluateExpressionDelegate:
        def anonymous_function(args: []):
            return bytes(args[0], encoding='UTF-8')

        return FunctionUtils.apply(anonymous_function, FunctionUtils.verify_string)
