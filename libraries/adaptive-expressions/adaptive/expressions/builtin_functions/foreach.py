from ..expression_evaluator import ExpressionEvaluator
from ..expression_type import FOREACH
from ..function_utils import FunctionUtils
from ..return_type import ReturnType


class Foreach(ExpressionEvaluator):
    def __init__(self):
        super().__init__(
            FOREACH,
            FunctionUtils.foreach,
            ReturnType.Array,
            FunctionUtils.validate_foreach,
        )
