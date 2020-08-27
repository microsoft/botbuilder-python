import numbers
import sys
from ..expression_evaluator import ExpressionEvaluator, EvaluateExpressionDelegate
from ..expression_type import ADD
from ..function_utils import FunctionUtils
from ..return_type import ReturnType


class Add(ExpressionEvaluator):
    def __init__(self):
        super().__init__(
            ADD, Add.evaluator(), ReturnType.String | ReturnType.Number, Add.validator
        )

    @staticmethod
    def evaluator() -> EvaluateExpressionDelegate:
        def anonymous_function(args: []):
            result: object = None
            error: str = None
            first_item = args[0]
            second_item = args[1]
            string_concat = not isinstance(
                first_item, numbers.Number
            ) or not isinstance(second_item, numbers.Number)

            if (
                first_item is None
                and isinstance(second_item, numbers.Number)
                or second_item is None
                and isinstance(first_item, numbers.Number)
            ):
                error = "Operator '+' or add cannot be applied to operands of type 'number' and null object."
            else:
                if string_concat:
                    if isinstance(
                        first_item, numbers.Number
                    ) and FunctionUtils.is_integer(first_item):
                        first_item = int(first_item)
                    if isinstance(
                        second_item, numbers.Number
                    ) and FunctionUtils.is_integer(second_item):
                        second_item = int(second_item)

                    result = (str(first_item) if first_item else "") + (
                        str(second_item) if second_item else ""
                    )
                else:
                    result = Add.eval_add(args[0], args[1])

            return result, error

        return FunctionUtils.apply_sequence_with_error(
            anonymous_function, FunctionUtils.verify_number_or_string_or_null
        )

    @staticmethod
    def eval_add(num_a: numbers.Number, num_b: numbers.Number):
        if num_a is None or num_b is None:
            raise Exception("Argument null exception.")

        return num_a + num_b

    @staticmethod
    def validator(expression: object):
        FunctionUtils.validate_arity_and_any_type(
            expression, 2, sys.maxsize, ReturnType.String | ReturnType.Number
        )
