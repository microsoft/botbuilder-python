from ..expression_evaluator import ExpressionEvaluator, EvaluateExpressionDelegate
from ..expression_type import ADDORDINAL
from ..function_utils import FunctionUtils
from ..return_type import ReturnType


class AddOrdinal(ExpressionEvaluator):
    def __init__(self):
        super().__init__(
            ADDORDINAL, AddOrdinal.evaluator(), ReturnType.Boolean, AddOrdinal.validator
        )

    @staticmethod
    def evaluator() -> EvaluateExpressionDelegate:
        def anonymous_function(args: list):
            result: object = None
            error: str = None
            input_var = 0
            input_var, error = FunctionUtils.parse_int(args[0])
            if error is None:
                result = AddOrdinal.eval_add_ordinal(input_var)
            return result, error

        return FunctionUtils.apply_with_error(
            anonymous_function, FunctionUtils.verify_integer
        )

    @staticmethod
    def validator(expression: object):
        FunctionUtils.validate_arity_and_any_type(expression, 1, 1, ReturnType.Number)

    @staticmethod
    def eval_add_ordinal(num: int):
        has_result = False
        ordinal_result = str(num)
        if num > 0:
            remain = num % 100
            if remain in (11, 12, 13):
                ordinal_result += "th"
                has_result = True
            if has_result is False:
                remain = num % 10
                if remain == 1:
                    ordinal_result += "st"
                elif remain == 2:
                    ordinal_result += "nd"
                elif remain == 3:
                    ordinal_result += "rd"
                else:
                    ordinal_result += "th"
        return ordinal_result
