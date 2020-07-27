from ..expression_evaluator import ExpressionEvaluator
from ..expression_type import NOT
from ..return_type import ReturnType
from ..options import Options
from ..function_utils import FunctionUtils


class Not(ExpressionEvaluator):
    def __init__(self):
        super().__init__(
            NOT, Not.evaluator, ReturnType.Boolean, FunctionUtils.validate_unary
        )

    @staticmethod
    def evaluator(expression, state, options: Options):
        result: object = None
        error: str = None
        options = Options(options)
        options.null_substitution = None
        result, error = expression.children[0].try_evaluate(state, options)
        if error is None:
            result = not FunctionUtils.is_logic_true(result)
        else:
            error = None
            result = True
        return result, error
