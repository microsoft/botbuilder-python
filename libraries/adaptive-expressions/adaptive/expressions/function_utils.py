import numbers
from typing import Callable, NewType
from .memory_interface import MemoryInterface
from .options import Options
from .return_type import ReturnType

VerifyExpression = NewType('VerifyExpression', Callable[[object, object, int], str])

class FunctionUtils:
    @staticmethod
    def validate_arity_and_any_type(expression: object, min_arity: int, max_arity: int, return_type: ReturnType = ReturnType.Object):
        if len(expression.children) < min_arity:
            raise Exception(expression + ' should have at least ' + str(min_arity) + ' children.')

        if len(expression.children) > max_arity:
            raise Exception(expression + ' can\'t have more than ' + str(max_arity) + ' children.')

        if return_type & ReturnType.Object == 0:
            for child in expression.children:
                if (child.return_type & ReturnType.Object == 0) and (return_type & child.return_type == 0):
                    #TODO: raise error with BuildTypeValidatorError
                    raise Exception('return type validation failed.')

    @staticmethod
    def verify_number_or_string_or_null(value: object, expression: object, number: int):
        error: str = None
        if not isinstance(value, numbers.Number) and not isinstance(value, str):
            error = expression + ' is not string or number'

        return error

    @staticmethod
    def apply_sequence_with_error(
        function: Callable[[list], object],
        verify: VerifyExpression = None):
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
        function: Callable[[list], object],
        verify: VerifyExpression = None):
        def anonymous_function(expression: object, state: MemoryInterface, options: Options):
            value: object
            error: str
            args: []
            args, error = FunctionUtils.evaluate_children(expression, state, options, verify)
            if error is None:
                try:
                    value, error = function(args)
                except Exception as err:
                    error = str(err)

            return value, error

        return anonymous_function

    @staticmethod
    def evaluate_children(expression: object, state: MemoryInterface, options: Options, verify: VerifyExpression = None):
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
            if index >= 0 and index < len(instance):
                value = instance[index]
            else:
                error = str(index) + ' is out of range for ' + instance
        else:
            error = instance + ' is not a collection.'

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
            prop = list(filter(lambda x: (x.lower() == property.lower()), instance_dict.keys()))
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
