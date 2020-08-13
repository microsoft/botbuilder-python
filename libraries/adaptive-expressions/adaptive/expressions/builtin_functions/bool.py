from ..expression_type import BOOL
from ..function_utils import FunctionUtils
from ..return_type import ReturnType
from .comparison_evaluator import ComparisonEvaluator

class Bool(ComparisonEvaluator):
    def __init__(self):
        super().__init__(
            BOOL, Bool.func, FunctionUtils.validate_unary
        )

    @staticmethod
    def func(args: []) -> bool:
            return FunctionUtils.is_logic_true(args[0])
