from typing import Callable
from ..expression_evaluator import ExpressionEvaluator
from ..function_utils import VerifyExpression, FunctionUtils
from ..return_type import ReturnType


class MultivariateNumericEvaluator(ExpressionEvaluator):
    def __init__(
        self,
        expr_type: str,
        function: Callable[[list], object],
        verify: VerifyExpression = None,
    ):
        super().__init__(
            expr_type,
            MultivariateNumericEvaluator.self_evaluator(function, verify),
            ReturnType.Number,
            FunctionUtils.validate_two_or_more_than_two_numbers,
        )

    @staticmethod
    def self_evaluator(
        function: Callable[[list], object], verify: VerifyExpression = None
    ):
        return FunctionUtils.apply_sequence(
            function, verify if verify is not None else FunctionUtils.verify_number,
        )
