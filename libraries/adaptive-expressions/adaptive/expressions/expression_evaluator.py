from typing import NewType, Callable
from .memory_interface import MemoryInterface
from .options import Options
from .return_type import ReturnType

EvaluatorLookup = NewType('EvaluatorLookup', Callable[[str], object])

EvaluateExpressionDelegate = NewType('EvaluateExpressionDelegate',
    Callable[[object, MemoryInterface, Options], object])

ValidateExpressionDelegate = NewType('ValidateExpressionDelegate', Callable[[object], object])

class ExpressionEvaluator:
    expr_type: str
    return_type: ReturnType

    _validator: ValidateExpressionDelegate
    _evaluator: EvaluateExpressionDelegate

    def __init__(self,
        expr_type: str,
        evaluator: EvaluateExpressionDelegate,
        return_type=ReturnType.Object,
        validator: ValidateExpressionDelegate = None):
        self.expr_type = expr_type
        self._evaluator = evaluator
        self.return_type = return_type
        self._validator = validator if validator is not None else lambda expr: None

    def try_evaluate(self, expression: object, state: MemoryInterface, options: Options):
        return self._evaluator(expression, state, options)

    def validate_expression(self, expression: object):
        self._validator(expression)
