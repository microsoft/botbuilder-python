from ..expression_evaluator import ExpressionEvaluator
from ..expression_type import COUNT
from ..function_utils import FunctionUtils
from ..return_type import ReturnType


class Count(ExpressionEvaluator):
    def __init__(self):
        super().__init__(
            COUNT, Count.evaluator(), ReturnType.Number, Count.validator,
        )

    @staticmethod
    def evaluator():
        def anonymous_function(args: list):
            count = None
            if isinstance(args[0], (str, list)):
                count = len(args[0])

            return count

        return FunctionUtils.apply(anonymous_function, FunctionUtils.verify_container)

    @staticmethod
    def validator(expression: object):
        FunctionUtils.validate_order(
            expression, None, ReturnType.String | ReturnType.Array
        )
