from .comparison_evaluator import ComparisonEvaluator
from ..expression_type import EQUAL
from ..function_utils import FunctionUtils


class Equal(ComparisonEvaluator):
    def __init__(self):
        super().__init__(EQUAL, FunctionUtils.is_equal, FunctionUtils.validate_binary)
