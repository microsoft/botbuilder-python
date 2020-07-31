from .comparison_evaluator import ComparisonEvaluator
from ..expression_type import EXIST
from ..function_utils import FunctionUtils


class Exist(ComparisonEvaluator):
    def __init__(self):
        super().__init__(
            EXIST,
            Exist.func,
            FunctionUtils.validate_unary,
            FunctionUtils.verify_not_null,
        )

    @staticmethod
    def func(args: list):
        return len(args) > 0 and args[0] is not None
