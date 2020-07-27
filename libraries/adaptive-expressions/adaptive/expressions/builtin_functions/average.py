import statistics
from ..expression_evaluator import ExpressionEvaluator, EvaluateExpressionDelegate
from ..expression_type import AVERAGE
from ..function_utils import FunctionUtils
from ..return_type import ReturnType


class Average(ExpressionEvaluator):
    def __init__(self):
        super().__init__(
            AVERAGE,
            Average.evaluator(),
            ReturnType.Number,
            FunctionUtils.validate_unary,
        )

    @staticmethod
    def evaluator() -> EvaluateExpressionDelegate:
        def anonymous_function(args: []):
            result = args[0]
            if isinstance(result, list):
                result = statistics.mean(result)

            return result

        return FunctionUtils.apply(
            anonymous_function, FunctionUtils.verify_numeric_list
        )
