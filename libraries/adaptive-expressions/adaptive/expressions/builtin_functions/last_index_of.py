from ..expression_evaluator import ExpressionEvaluator
from ..expression_type import LASTINDEXOF
from ..function_utils import FunctionUtils
from ..return_type import ReturnType
from ..options import Options


class LastIndexOf(ExpressionEvaluator):
    def __init__(self):
        super().__init__(
            LASTINDEXOF, LastIndexOf.evaluator, ReturnType.Number, LastIndexOf.validator
        )

    @staticmethod
    def evaluator(expression: object, state, options: Options):
        result = -1
        args, error = FunctionUtils.evaluate_children(expression, state, options)
        if error is None:
            if isinstance(args[0], str) or args[0] is None:
                if isinstance(args[1], str) or args[1] is None:
                    args[0] = args[0] if isinstance(args[0], str) else ""
                    args[1] = args[1] if isinstance(args[1], str) else ""
                    result = str(args[0][::-1]).find(args[1])
                    result = -1 if result == -1 else len(args[0]) - result - 1
                else:
                    error = (
                        "Can only look for indexof string in " + expression.to_string()
                    )
            elif isinstance(args[0], list):
                for i, arg in enumerate(list(args[0])[::-1]):
                    if args[1] == arg:
                        result = len(args[0]) - i - 1
                        break
            else:
                error = "{" + expression.to_string() + "} works only on string or list."
        return result, error

    @staticmethod
    def validator(expression: object):
        FunctionUtils.validate_order(
            expression, None, ReturnType.Array | ReturnType.String, ReturnType.Object
        )
