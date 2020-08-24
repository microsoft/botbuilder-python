import demjson
from ..expression_type import JSON
from ..function_utils import FunctionUtils
from ..return_type import ReturnType
from ..expression_evaluator import ExpressionEvaluator, EvaluateExpressionDelegate


class Json(ExpressionEvaluator):
    def __init__(self):
        super().__init__(
            JSON, Json.evaluator(), ReturnType.Object, Json.validator,
        )

    @staticmethod
    def evaluator() -> EvaluateExpressionDelegate:
        def anonymous_function(args: list):
            return demjson.decode(args[0])

        return FunctionUtils.apply(anonymous_function)

    @staticmethod
    def validator(expression: object):
        FunctionUtils.validate_order(expression, None, ReturnType.String)
