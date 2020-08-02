from ..options import Options
from ..expression_evaluator import ExpressionEvaluator
from ..expression_type import SUBSTRING
from ..function_utils import FunctionUtils
from ..return_type import ReturnType

class SubString(ExpressionEvaluator):
    def __init__(self):
        super().__init__(
            SUBSTRING, SubString.eval_substring, ReturnType.String, SubString.validator
        )

    @staticmethod
    def eval_substring(expression: object, state, options: Options):
        result: str = None
        error: str
        result: str
        result, error = expression.children[0].try_evaluate(state, options)
        if error is None:
            if result is None:
                result = ""
            else:
                start: int
                start_expr = expression.children[1]
                start, error = start_expr.try_evaluate(state, options)
                if error is None and (start < 0 or start >= len(result)):
                    error = "{" + start_expr + "}={" + start + "} which is out of range for {" + result + "}."
                if error is None:
                    length: int
                    if len(expression.children) == 2:
                        # Without length, compute to end
                        length = len(result) - start
                    else:
                        length_expr = expression.children[2]
                        length, error = length_expr.try_evaluate(state, options)
                        if error is None and (length < 0 or start + length > len(result)):
                            error = "{" + length_expr + "}={" + length + "} which is out of range for {" + result + "}."
                    if error is None:
                        result = result[int(start): int(start + length)]
        return result, error

    @staticmethod
    def validator(expression: object):
        FunctionUtils.validate_order(expression, [ReturnType.Number], ReturnType.String, ReturnType.Number)
