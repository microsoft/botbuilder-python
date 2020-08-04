from ..expression_evaluator import ExpressionEvaluator
from ..expression_type import INDICESANDVALUES
from ..function_utils import FunctionUtils
from ..return_type import ReturnType
from ..memory_interface import MemoryInterface
from ..options import Options


class IndicesAndValues(ExpressionEvaluator):
    def __init__(self):
        super().__init__(
            INDICESANDVALUES,
            IndicesAndValues.evaluator,
            ReturnType.Array,
            FunctionUtils.validate_unary,
        )

    @staticmethod
    def evaluator(expression: object, state: MemoryInterface, options: Options):
        result: object = None
        error: str = None
        value: object = None

        value, error = expression.children[0].try_evaluate(state, options)
        if error is None:
            if isinstance(value, (list, set)):
                temp_list = []
                for i, item in enumerate(value):
                    temp_list.append({"index": i, "value": item})

                result = temp_list
            elif isinstance(value, dict):
                temp_list = []
                for key in value:
                    temp_list.append({"index": key, "value": value[key]})

                result = temp_list
            else:
                error = expression.children[0].to_string() + " is not array or object."

        value = result

        return value, error
