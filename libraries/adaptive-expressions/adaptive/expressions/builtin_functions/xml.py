import json
import xmltodict
from ..expression_evaluator import ExpressionEvaluator, EvaluateExpressionDelegate
from ..expression_type import XML
from ..function_utils import FunctionUtils
from ..return_type import ReturnType


class Xml(ExpressionEvaluator):
    def __init__(self):
        super().__init__(
            XML, Xml.evaluator(), ReturnType.String, FunctionUtils.validate_unary
        )

    @staticmethod
    def evaluator() -> EvaluateExpressionDelegate:
        def anonymous_function(args: []):
            json_date: object = args[0]
            if isinstance(args[0], str):
                json_date = json.loads(args[0])
            return xmltodict.unparse(json_date).replace('\n', '').replace('\r', '')

        return FunctionUtils.apply(anonymous_function)
