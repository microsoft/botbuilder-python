from ..expression_evaluator import ExpressionEvaluator
from ..expression_type import AND
from ..options import Options
from ..function_utils import FunctionUtils
from ..return_type import ReturnType

class And(ExpressionEvaluator):
    def __init__(self):
        super().__init__(
            AND, And.evaluator, ReturnType.Boolean, FunctionUtils.validate_at_least_one
        )

    @staticmethod
    def evaluator(expression, state, options: Options):
        result: object = True
        error: str = None
        for child in expression.children:
            options = Options(options)
            options.null_substitution = None
            result, error = child.try_evaluate(state, options)
            if error is None:
                if FunctionUtils.is_logic_true(result):
                    result = True
                else:
                    result = False
                    break
            else:
                # We interpret any error as flase and swallow the error
                result = False
                error = None
                break
        return result, error
