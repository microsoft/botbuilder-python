from ..expression_evaluator import ExpressionEvaluator
from ..expression_type import CONTAINS
from ..function_utils import FunctionUtils
from ..return_type import ReturnType
from ..memory_interface import MemoryInterface
from ..options import Options


class Contains(ExpressionEvaluator):
    def __init__(self):
        super().__init__(
            CONTAINS,
            Contains.evaluator,
            ReturnType.Boolean,
            FunctionUtils.validate_binary,
        )

    @staticmethod
    def evaluator(expression: object, state: MemoryInterface, options: Options):
        found = False
        args, error = FunctionUtils.evaluate_children(expression, state, options)
        if error is None:
            if (
                isinstance(args[0], str)
                and isinstance(args[1], str)
                or isinstance(args[0], (list, dict))
            ):
                found = args[1] in args[0]

        return found, None
