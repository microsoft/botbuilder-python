from ..expression_evaluator import ExpressionEvaluator
from ..expression_type import ELEMENT
from ..options import Options
from ..function_utils import FunctionUtils
from ..return_type import ReturnType
from ..memory_interface import MemoryInterface


class Element(ExpressionEvaluator):
    def __init__(self):
        super().__init__(
            ELEMENT, Element.evaluator, ReturnType.Object, FunctionUtils.validate_binary
        )

    @staticmethod
    def evaluator(expression: object, state: MemoryInterface, options: Options):
        value: object = None
        error: str = None
        instance = expression.children[0]
        index = expression.children[1]
        inst: object

        res = instance.try_evaluate(state, options)
        inst = res[0]
        error = res[1]

        if error is None:
            idx_value: object
            new_options = Options(options)
            new_options.null_substitution = None
            res = index.try_evaluate(state, new_options)
            idx_value = res[0]
            error = res[1]
            if error is None:
                if FunctionUtils.is_integer(idx_value):
                    value, error = FunctionUtils.access_index(inst, int(idx_value))
                elif isinstance(idx_value, str):
                    value, error = FunctionUtils.access_property(inst, idx_value)
                else:
                    error = (
                        "Could not coerce "
                        + index.to_string()
                        + " to an int or string."
                    )

                return value, error

        return value, error
