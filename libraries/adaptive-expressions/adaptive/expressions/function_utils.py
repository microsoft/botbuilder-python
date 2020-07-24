import numbers
import sys
from typing import Callable, NewType
from .memory_interface import MemoryInterface
from .options import Options
from .return_type import ReturnType

VerifyExpression = NewType("VerifyExpression", Callable[[object, object, int], str])

# pylint: disable=unused-argument
class FunctionUtils:
    verify_expression = VerifyExpression

    @staticmethod
    def validate_arity_and_any_type(
        expression: object,
        min_arity: int,
        max_arity: int,
        return_type: ReturnType = ReturnType.Object,
    ):
        if len(expression.children) < min_arity:
            raise Exception(
                expression + " should have at least " + str(min_arity) + " children."
            )

        if len(expression.children) > max_arity:
            raise Exception(
                expression + " can't have more than " + str(max_arity) + " children."
            )

        if return_type & ReturnType.Object == 0:
            for child in expression.children:
                if (child.return_type & ReturnType.Object == 0) and (
                    return_type & child.return_type == 0
                ):
                    # TODO: raise error with BuildTypeValidatorError
                    raise Exception("return type validation failed.")

    @staticmethod
    def validate_binary(expression: object):
        FunctionUtils.validate_arity_and_any_type(expression, 2, 2)

    @staticmethod
    def validate_two_or_more_than_two_numbers(expression: object):
        FunctionUtils.validate_arity_and_any_type(
            expression, 2, sys.maxsize, ReturnType.Number
        )

    @staticmethod
    def validate_binary_number_or_string(expression: object):
        FunctionUtils.validate_arity_and_any_type(
            expression, 2, 2, ReturnType.Number | ReturnType.String
        )

    @staticmethod
    # pylint: disable=unused-argument
    def validate_at_least_one(expression: object):
        return FunctionUtils.validate_arity_and_any_type(expression, 1, sys.maxsize)

    @staticmethod
    def verify_number_or_string_or_null(value: object, expression: object, number: int):
        error: str = None
        if not isinstance(value, numbers.Number) and not isinstance(value, str):
            error = expression + " is not string or number"

        return error

    @staticmethod
    def verify_numbers(value: object, expression: object, pos: int):
        error: str = None
        if not isinstance(value, numbers.Number):
            error = expression + " is not a number."

        return error

    @staticmethod
    def verify_numeric_list_or_number(value: object, expression: object, number: int):
        error: str = None
        if isinstance(value, numbers.Number):
            return error

        if not isinstance(value, list):
            error = expression + " is neither a list nor a number."
        else:
            for elt in value:
                if not isinstance(elt, numbers.Number):
                    error = elt + " is not a number in " + expression
                    break

        return error

    @staticmethod
    def apply_sequence_with_error(
        function: Callable[[list], object], verify: VerifyExpression = None
    ):
        def anonymous_function(args: []) -> object:
            binary_args = [None, None]
            so_far = args[0]
            value: object
            error: str
            for arg in args[1:]:
                binary_args[0] = so_far
                binary_args[1] = arg
                value, error = function(binary_args)
                if error:
                    return value, error

                so_far = value

            value = so_far
            error = None
            return value, error

        return FunctionUtils.apply_with_error(anonymous_function, verify)

    @staticmethod
    def apply_with_error(
        function: Callable[[list], object], verify: VerifyExpression = None
    ):
        def anonymous_function(
            expression: object, state: MemoryInterface, options: Options
        ):
            value: object
            error: str
            args: []
            args, error = FunctionUtils.evaluate_children(
                expression, state, options, verify
            )
            if error is None:
                try:
                    value, error = function(args)
                except Exception as err:
                    error = str(err)

            return value, error

        return anonymous_function

    @staticmethod
    def apply_sequence(
        function: Callable[[list], object], verify: VerifyExpression = None
    ):
        def anonymous_function(args: list):
            binary_args = [None, None]
            so_far = args[0]
            for arg in args[1:]:
                binary_args[0] = so_far
                binary_args[1] = arg
                so_far = function(binary_args)

            return so_far

        return FunctionUtils.apply(anonymous_function, verify)

    @staticmethod
    def apply(function: Callable[[list], object], verify: VerifyExpression = None):
        def anonymous_function(
            expression: object, state: MemoryInterface, options: Options
        ):
            value: object
            error: str
            args: []
            args, error = FunctionUtils.evaluate_children(
                expression, state, options, verify
            )
            if error is None:
                try:
                    value = function(args)
                except Exception as err:
                    error = str(err)

            return value, error

        return anonymous_function

    @staticmethod
    def evaluate_children(
        expression: object,
        state: MemoryInterface,
        options: Options,
        verify: VerifyExpression = None,
    ):
        args = []
        value: object
        error: str
        pos = 0

        for child in expression.children:
            res = child.try_evaluate(state, options)
            value = res[0]
            error = res[1]
            if error:
                break

            if verify:
                error = verify(value, child, pos)

            if error:
                break

            args.append(value)
            pos = pos + 1

        return args, error

    @staticmethod
    def access_index(instance: object, index: int):
        value: object = None
        error: str = None

        if instance is None:
            return value, error

        if isinstance(instance, list):
            if 0 <= index < len(instance):
                value = instance[index]
            else:
                error = str(index) + " is out of range for " + instance
        else:
            error = instance + " is not a collection."

        return value, error

    @staticmethod
    def access_property(instance: object, property: str):
        value: object = None
        error: str = None

        if instance is None:
            return value, error

        instance_dict = dict(instance)
        value = instance_dict.get(property)
        if value is None:
            prop = list(
                filter(lambda x: (x.lower() == property.lower()), instance_dict.keys())
            )
            if len(prop) > 0:
                value = instance_dict.get(prop[0])

        return value, error

    @staticmethod
    def set_property(instance: object, property: str, val: object):
        result = val
        instance[property] = val
        value = result
        error = None
        return value, error

    @staticmethod
    def try_parse_list(value: object, out_list: list):
        islist = False
        out_list.clear()
        if isinstance(value, list):
            for i in list(value):
                out_list.append(i)
            islist = True
        return islist

    @staticmethod
    def culture_invariant_double_convert(number: object):
        return float(number)
