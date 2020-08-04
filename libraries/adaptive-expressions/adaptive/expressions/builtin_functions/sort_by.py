from ..expression_evaluator import ExpressionEvaluator
from ..expression_type import SORTBY
from ..function_utils import FunctionUtils
from ..return_type import ReturnType


class SortBy(ExpressionEvaluator):
    def __init__(self):
        super().__init__(
            SORTBY, FunctionUtils.sort_by(False), ReturnType.Array, SortBy.validator,
        )

    @staticmethod
    def validator(expression: object):
        FunctionUtils.validate_order(expression, [ReturnType.String], ReturnType.Array)
