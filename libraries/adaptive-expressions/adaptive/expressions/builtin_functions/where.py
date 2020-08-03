from ..expression_evaluator import ExpressionEvaluator
from ..expression_type import WHERE
from ..function_utils import FunctionUtils
from ..return_type import ReturnType
from ..memory_interface import MemoryInterface
from ..options import Options
from ..memory import SimpleObjectMemory
from ..memory import StackedMemory


class Where(ExpressionEvaluator):
    def __init__(self):
        super().__init__(
            WHERE, Where.evaluator, ReturnType.Array, FunctionUtils.validate_foreach,
        )

    @staticmethod
    def evaluator(expression: object, state: MemoryInterface, options: Options):
        result: object = None
        error: str = None
        instance: object = None

        res = expression.children[0].try_evaluate(state, options)
        instance = res[0]
        error = res[1]

        if error is None:
            iterator_name = str(expression.children[1].children[0].get_value())
            arr = []
            is_instance_array = False
            if isinstance(instance, (list, set)):
                arr = instance
                is_instance_array = True
            elif isinstance(instance, dict):
                for ele in instance:
                    arr.append({"key": ele, "value": instance[ele]})
            else:
                error = (
                    expression.children[0].to_string()
                    + " is not a collection or structure object to run foreach"
                )

            if error is None:
                stacked_memory = StackedMemory.wrap(state)
                arr_result = []
                for item in arr:
                    local = {iterator_name: item}
                    stacked_memory.append(SimpleObjectMemory.wrap(local))
                    new_options = Options(options)
                    new_options.null_substitution = None
                    res = expression.children[2].try_evaluate(
                        stacked_memory, new_options
                    )
                    stacked_memory.pop()

                    if FunctionUtils.is_logic_true(res[0]) and res[1] is None:
                        arr_result.append(local.get(iterator_name))

                if not is_instance_array:
                    obj_result = {}
                    for item in arr_result:
                        obj_result[item["key"]] = item["value"]

                    result = obj_result
                else:
                    result = arr_result

        value = result

        return value, error
