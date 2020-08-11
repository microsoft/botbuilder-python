from ..options import Options
from ..expression_type import TICKS
from ..function_utils import FunctionUtils
from ..return_type import ReturnType
from ..expression_evaluator import ExpressionEvaluator


class Ticks(ExpressionEvaluator):
    def __init__(self):
        super().__init__(TICKS, Ticks.evaluator, ReturnType.Number, Ticks.validator)

    @staticmethod
    def evaluator(expression: object, state, options: Options):
        value: object = None
        error: str = None
        args: list
        args, error = FunctionUtils.evaluate_children(expression, state, options)
        if error is None:
            value, error = FunctionUtils.ticks_with_error(args[0])
        return value, error

    @staticmethod
    def validator(expression: object):
        FunctionUtils.validate_arity_and_any_type(expression, 1, 1, ReturnType.String)
