import numbers
from typing import Callable
from ..expression_evaluator import (
    ExpressionEvaluator,
    EvaluateExpressionDelegate,
    ValidateExpressionDelegate,
)
from ..options import Options
from ..function_utils import FunctionUtils
from ..return_type import ReturnType


class ComparisonEvaluator(ExpressionEvaluator):
    def __init__(
        self,
        expr_type: str,
        func: Callable[[list], bool],
        validator: ValidateExpressionDelegate,
        verify: FunctionUtils.verify_expression = None,
    ):
        super().__init__(
            expr_type,
            ComparisonEvaluator.evaluator(func, verify),
            ReturnType.Boolean,
            validator,
        )

    @staticmethod
    def evaluator(
        func: Callable[[list], bool], verify: FunctionUtils.verify_expression
    ) -> EvaluateExpressionDelegate:
        def anonymous_function(expression, state, options: Options):
            result = False
            error: str = None
            args: list
            options = Options(options)
            options.null_substitution = None
            args, error = FunctionUtils.evaluate_children(
                expression, state, options, verify
            )
            if error is None:
                is_number: bool = None
                for arg in args:
                    obj = arg
                    if is_number is not None:
                        if (
                            obj is not None
                            and isinstance(obj, numbers.Number) != is_number
                        ):
                            error = (
                                "Arguments must either all be numbers or strings in "
                                + str(expression)
                                + "}"
                            )
                            break
                    else:
                        is_number = isinstance(obj, numbers.Number)
                if error is None:
                    try:
                        result = func(args)
                    except Exception as err:
                        error = str(err)

            else:
                error = None
            return result, error

        return anonymous_function
