from typing import Callable
from ..expression_evaluator import ExpressionEvaluator
from ..function_utils import FunctionUtils
from ..return_type import ReturnType


class NumberTransformEvaluator(ExpressionEvaluator):
    def __init__(
        self, expr_type: str, function: Callable[[list], object],
    ):
        super().__init__(
            expr_type,
            NumberTransformEvaluator.self_evaluator(function),
            ReturnType.Number,
            FunctionUtils.validate_unary_number,
        )

    @staticmethod
    def self_evaluator(function: Callable[[list], object],):
        return FunctionUtils.apply(function, FunctionUtils.verify_number)
