from ..expression_evaluator import ExpressionEvaluator
from ..expression_type import OR
from ..options import Options
from ..function_utils import FunctionUtils
from ..return_type import ReturnType


class Or(ExpressionEvaluator):
    def __init__(self):
        super().__init__(
            OR, Or.evaluator, ReturnType.Boolean, FunctionUtils.validate_at_least_one
        )

    @staticmethod
    def evaluator(expression, state, options: Options):
        for child in expression.children:
            options = Options(options)
            options.null_substitution = None
            result, error = child.try_evaluate(state, options)
            if error is None:
                if FunctionUtils.is_logic_true(result):
                    result = True
                    break
            else:
                error = None
        return result, error
