from ..expression_evaluator import ExpressionEvaluator
from ..expression_type import ACCESSOR
from ..options import Options
from ..function_utils import FunctionUtils
from ..return_type import ReturnType
from ..memory_interface import MemoryInterface
from ..memory import SimpleObjectMemory


class Accessor(ExpressionEvaluator):
    def __init__(self):
        super().__init__(
            ACCESSOR, Accessor.evaluator, ReturnType.Object, Accessor.validator
        )

    @staticmethod
    def evaluator(expression: object, state: MemoryInterface, options: Options):
        value: object = None
        error: str = None

        path, left, error = FunctionUtils.try_accumulate_path(
            expression, state, options
        )

        if error is not None:
            return value, error

        if left is None:
            value = FunctionUtils.wrap_get_value(state, path, options)
            return value, error
        else:
            res = left.try_evaluate(state, options)
            new_scope = res.value
            error = res.error

            if error is not None:
                return value, error

            value = FunctionUtils.wrap_get_value(
                SimpleObjectMemory(new_scope), path, options
            )

            return value, error

    @staticmethod
    def validator(expression: object):
        # pylint: disable=import-outside-toplevel
        from ..constant import Constant

        children = expression.children
        if (
            len(children) == 0
            or not isinstance(children[0], Constant)
            or children[0].return_type != ReturnType.String
        ):
            raise Exception(expression + " must have a string as first argument.")

        if len(children) > 2:
            raise Exception(expression + " has more than 2 children.")

        if len(children) == 2 and (children[1].return_type & ReturnType.Object) == 0:
            raise Exception(expression + " must have an object as its second argument.")
