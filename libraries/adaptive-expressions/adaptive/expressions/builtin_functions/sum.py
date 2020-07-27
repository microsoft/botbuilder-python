from ..expression_evaluator import ExpressionEvaluator, EvaluateExpressionDelegate
from ..expression_type import SUM
from ..function_utils import FunctionUtils
from ..return_type import ReturnType


class Sum(ExpressionEvaluator):
    def __init__(self):
        super().__init__(SUM, Sum.evaluator(), ReturnType.Number, Sum.validator)

    @staticmethod
    def evaluator() -> EvaluateExpressionDelegate:
        def anonymous_function(args: []):
            result = args[0]
            if isinstance(result, list):
                result = sum(result)

            return result

        return FunctionUtils.apply(
            anonymous_function, FunctionUtils.verify_numeric_list
        )

    @staticmethod
    def validator(expression: object):
        FunctionUtils.validator_order(expression, None, ReturnType.Array)
