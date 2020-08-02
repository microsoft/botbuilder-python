from ..expression_evaluator import ExpressionEvaluator
from ..expression_type import JOIN
from ..function_utils import FunctionUtils
from ..return_type import ReturnType
from ..memory_interface import MemoryInterface
from ..options import Options


class Join(ExpressionEvaluator):
    def __init__(self):
        super().__init__(
            JOIN, Join.eval_join, ReturnType.String, Join.validator,
        )

    @staticmethod
    def eval_join(expression: object, state: MemoryInterface, options: Options):
        value: object = None
        args, error = FunctionUtils.evaluate_children(expression, state, options)
        if error is None:
            if not isinstance(args[0], list):
                error = (
                    expression.children[0].to_string()
                    + " evaluates to "
                    + str(args[0])
                    + " which is not a list."
                )
            else:
                if len(args) == 2:
                    value = str(args[1]).join(map(str, args[0]))
                else:
                    if len(args[0]) < 3:
                        value = str(args[2]).join(map(str, args[0]))
                    else:
                        first_part = str(args[1]).join(map(str, args[0][0:-1]))
                        value = first_part + str(args[2]) + str(args[0][-1])

        return value, error

    @staticmethod
    def validator(expression: object):
        FunctionUtils.validate_order(
            expression, [ReturnType.String], ReturnType.Array, ReturnType.String
        )
