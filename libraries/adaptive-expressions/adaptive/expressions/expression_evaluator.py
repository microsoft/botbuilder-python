from typing import NewType, Callable

from .expression import Expression, ReturnType
from .memory.memory_interface import MemoryInterface
from .options import Options

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

    def try_evaluate(self, expression: Expression, state: MemoryInterface, options: Options):
        return self._evaluator(expression, state, options)

    def validate_expression(self, expression: Expression):
        self._validator(expression)

EvaluatorLookup = NewType('EvaluatorLookup', Callable[[str], ExpressionEvaluator])

EvaluateExpressionDelegate = NewType('EvaluateExpressionDelegate',
    Callable[[Expression, MemoryInterface, Options], object])

ValidateExpressionDelegate = NewType('ValidateExpressionDelegate', Callable[[Expression], object])
