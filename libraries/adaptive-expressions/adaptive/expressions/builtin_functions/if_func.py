from ..expression_evaluator import ExpressionEvaluator
from ..expression_type import IF
from ..function_utils import FunctionUtils
from ..return_type import ReturnType
from ..memory_interface import MemoryInterface
from ..options import Options


class If(ExpressionEvaluator):
    def __init__(self):
        super().__init__(
            IF, If.evaluator, ReturnType.Object, If.validator,
        )

    @staticmethod
    def evaluator(expression: object, state: MemoryInterface, options: Options):
        value: object = None
        error: str = None
        new_options = Options(options)
        new_options.null_substitution = None
        res = expression.children[0].try_evaluate(state, new_options)
        value = res[0]
        error = res[1]
        if not error and FunctionUtils.is_logic_true(value):
            res = expression.children[1].try_evaluate(state, options)
        else:
            res = expression.children[2].try_evaluate(state, options)

        value = res[0]
        error = res[1]

        return value, error

    @staticmethod
    def validator(expr: object):
        FunctionUtils.validate_arity_and_any_type(expr, 3, 3)
