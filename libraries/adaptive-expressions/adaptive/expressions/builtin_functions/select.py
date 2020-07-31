from ..expression_evaluator import ExpressionEvaluator
from ..expression_type import SELECT
from ..function_utils import FunctionUtils
from ..return_type import ReturnType


class Select(ExpressionEvaluator):
    def __init__(self):
        super().__init__(
            SELECT,
            FunctionUtils.foreach,
            ReturnType.Array,
            FunctionUtils.validate_foreach,
        )
