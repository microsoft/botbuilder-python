from ..expression_evaluator import ExpressionEvaluator, EvaluateExpressionDelegate
from ..expression_type import DATAURITOSTRING
from ..function_utils import FunctionUtils
from ..return_type import ReturnType
import base64


class DataUriToString(ExpressionEvaluator):
    def __init__(self):
        super().__init__(
            DATAURITOSTRING, DataUriToString.evaluator(), ReturnType.String, FunctionUtils.validate_unary
        )

    @staticmethod
    def evaluator() -> EvaluateExpressionDelegate:
        def anonymous_function(args: []):
            base64String: str = args[0][args[0].index(',') + 1:]
            return base64.b64decode(base64String).decode()

        return FunctionUtils.apply(anonymous_function, FunctionUtils.verify_string)
