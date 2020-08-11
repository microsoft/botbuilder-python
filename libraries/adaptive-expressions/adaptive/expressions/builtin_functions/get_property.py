from ..options import Options
from ..memory import SimpleObjectMemory
from ..expression_type import GETPROPERTY
from ..function_utils import FunctionUtils
from ..return_type import ReturnType
from ..expression_evaluator import ExpressionEvaluator


class GetProperty(ExpressionEvaluator):
    def __init__(self):
        super().__init__(
            GETPROPERTY,
            GetProperty.evaluator,
            ReturnType.Object,
            GetProperty.validator,
        )

    @staticmethod
    def evaluator(expression: object, state, options: Options):
        value: object = None
        error: str
        first_item: object
        prop: object

        children = expression.children
        first_item, error = children[0].try_evaluate(state, options)
        if error is None:
            if len(children) == 1:
                # get root value from memory
                if not isinstance(first_item, str):
                    error = (
                        "Single parameter {"
                        + children[0].to_string()
                        + "} is not a string."
                    )
                else:
                    value = FunctionUtils.wrap_get_value(state, first_item, options)
            else:
                # get the property value from the instance
                prop, error = children[1].try_evaluate(state, options)
                print(SimpleObjectMemory(first_item))
                if error is None:
                    value = FunctionUtils.wrap_get_value(
                        SimpleObjectMemory(first_item), str(prop), options
                    )

        return value, error

    @staticmethod
    def validator(expression: object):
        FunctionUtils.validate_order(expression, [ReturnType.String], ReturnType.Object)
