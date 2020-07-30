import numbers
import sys
from collections.abc import Iterable
from typing import Callable, NewType
from .memory_interface import MemoryInterface
from .options import Options
from .return_type import ReturnType
from .expression_type import ACCESSOR, ELEMENT

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
                    raise Exception(
                        FunctionUtils.build_type_validator_error(
                            return_type, child, expression
                        )
                    )

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
    def validate_at_least_one(expression: object):
        return FunctionUtils.validate_arity_and_any_type(expression, 1, sys.maxsize)

    @staticmethod
    def validate_unary(expression: object):
        return FunctionUtils.validate_arity_and_any_type(expression, 1, 1)

    @staticmethod
    def validate_binary_number(expression: object):
        return FunctionUtils.validate_arity_and_any_type(
            expression, 2, 2, ReturnType.Number
        )

    @staticmethod
    def validate_order(expression: object, optional: list, *types: object):
        if optional is None:
            optional = []
        if len(expression.children) < len(types) or len(expression.children) > len(
            types
        ) + len(optional):
            if len(optional) == 0:

                raise Exception(
                    "{"
                    + expression.to_string()
                    + "} should have {"
                    + str(len(types))
                    + "} children."
                )

            raise Exception(
                "{"
                + expression.to_string()
                + "} should have between {"
                + str(len(types))
                + "} and {"
                + str(len(types) + len(optional))
                + "} children."
            )

        for i, child_type in enumerate(types):
            child = expression.children[i]
            child_return_type = child.return_type

            if (
                child_type & ReturnType.Object == 0
                and child_return_type & ReturnType.Object == 0
                and child_type & child_return_type == 0
            ):

                raise Exception(
                    FunctionUtils.build_type_validator_error(
                        child_type, child, expression
                    )
                )
        for i, child_type in enumerate(optional):
            i_c = i + len(types)
            if i_c >= len(expression.children):
                break
            child = expression.children[i_c]
            child_return_type = child.return_type()

            if (
                child_type & ReturnType.Object == 0
                and child_return_type & ReturnType.Object == 0
                and child_type & child_return_type == 0
            ):

                raise Exception(
                    FunctionUtils.build_type_validator_error(
                        child_type, child, expression
                    )
                )

    @staticmethod
    def validate_unary_number(expression: object):
        return FunctionUtils.validate_arity_and_any_type(
            expression, 1, 1, ReturnType.Number
        )

    @staticmethod
    def validate_unary_or_binary_number(expression: object):
        return FunctionUtils.validate_arity_and_any_type(
            expression, 1, 2, ReturnType.Number
        )

    @staticmethod
    def validate_unary_string(expression: object):
        return FunctionUtils.validate_arity_and_any_type(
            expression, 1, 1, ReturnType.String
        )

    @staticmethod
    def verify_string_or_null(value: object, expression: object, number: int):
        error: str = None
        if not isinstance(value, str) and value is not None:
            error = expression.to_string() + " is neither a string nor a null object."
        return error

    @staticmethod
    def verify_number_or_string_or_null(value: object, expression: object, number: int):
        error: str = None
        if not isinstance(value, numbers.Number) and not isinstance(value, str):
            error = expression + " is not string or number"

        return error

    @staticmethod
    def verify_number(value: object, expression: object, pos: int):
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
    def verify_integer(value: object, expression: object, number: int):
        error: str = None
        if isinstance(value, int):
            error = expression + " is not an integer."

        return error

    @staticmethod
    def verify_numeric_list(value: object, expression: object, number: int):
        error: str = None
        if not isinstance(value, list):
            error = expression + " is not a list."
        else:
            for elt in value:
                if not isinstance(elt, numbers.Number):
                    error = elt + " is not a number in " + expression
                    break

        return error

    @staticmethod
    def verify_not_null(value: object, expression, number: int):
        error: str = None
        if value is not None:
            error = expression.to_string() + " is null."
        return error

    @staticmethod
    def verify_container(value: object, expression: object, number: int):
        error: str = None
        if not isinstance(value, str) and not isinstance(value, Iterable):
            error = expression + " must be a string or list."

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
            value: object = None
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
        error: str = None
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
    def parse_int(obj: object):
        result: int = 0
        error: str = None
        if not obj.is_integer():
            error = str(obj) + " must be a integer."
        else:
            result = int(obj)

        return result, error

    @staticmethod
    def is_logic_true(instance: object):
        result = True
        if isinstance(instance, bool):
            result = instance
        elif instance is None:
            result = False
        return result

    @staticmethod
    def try_accumulate_path(
        expression: object, state: MemoryInterface, options: Options
    ):
        path: str = ""
        error: str = None
        left = expression
        while left is not None:
            if left.expr_type == ACCESSOR:
                path = str(left.children[0].get_value()) + "." + path
                left = left.children[1] if len(left.children) == 2 else None
            elif left.expr_type == ELEMENT:
                value, error = left.children[1].try_evaluate(state, options)

                if error is not None:
                    path = None
                    left = None
                    return path, left, error

                if isinstance(value, numbers.Number) and value.is_integer():
                    path = "[" + len(int(value)) + "]." + path
                elif isinstance(value, str):
                    path = "['" + value + "']." + path
                else:
                    path = None
                    left = None
                    error = (
                        left.children[1].to_string()
                        + " doesn't return an int or string"
                    )
                    return path, left, error

                left = left.children[0]
            else:
                break

        path = path.rstrip(".").replace(".[", "[")
        if path == "":
            path = None

        return path, left, error

    @staticmethod
    def wrap_get_value(state: MemoryInterface, path: str, options: Options):
        result = state.get_value(path)
        if result is not None:
            return result

        if options.null_substitution is not None:
            return options.null_substitution(path)

        return None

    @staticmethod
    def build_type_validator_error(
        return_type: ReturnType, child_expr: object, expr: object
    ):
        result: str
        names: str
        if return_type == (1,):
            names = "Boolean"
        elif return_type == (2,):
            names = "Number"
        elif return_type == (4,):
            names = "Object"
        elif return_type == (8,):
            names = "String"
        else:
            names = "Array"
        if not "," in names:
            result = (
                "{"
                + child_expr.to_string()
                + "} is not a {"
                + names
                + "} expression in {"
                + expr.to_string()
                + "}."
            )
        else:
            result = (
                "{"
                + child_expr.to_string()
                + "} in {"
                + expr.to_string()
                + "} is not any of [{"
                + names
                + "}]."
            )
        return result
