from typing import Callable
from ..expression_evaluator import ExpressionEvaluator
from ..function_utils import FunctionUtils
from ..return_type import ReturnType


class StringTransformEvaluator(ExpressionEvaluator):
    def __init__(self, type: str, func: Callable[[list], object]):
        super().__init__(
            type,
            StringTransformEvaluator.evaluator(func),
            ReturnType.String,
            FunctionUtils.validate_unary_string,
        )

    @staticmethod
    def evaluator(func: Callable[[list], object]):
        return FunctionUtils.apply(func, FunctionUtils.verify_string_or_null)
