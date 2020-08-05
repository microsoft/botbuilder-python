from ..expression_evaluator import ExpressionEvaluator
from ..expression_type import SORTBYDESCENDING
from ..function_utils import FunctionUtils
from ..return_type import ReturnType


class SortByDescending(ExpressionEvaluator):
    def __init__(self):
        super().__init__(
            SORTBYDESCENDING,
            FunctionUtils.sort_by(True),
            ReturnType.Array,
            SortByDescending.validator,
        )

    @staticmethod
    def validator(expression: object):
        FunctionUtils.validate_order(expression, [ReturnType.String], ReturnType.Array)
