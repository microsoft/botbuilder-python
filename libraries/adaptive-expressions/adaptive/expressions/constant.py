import numbers
import expression as expr
import expression_evaluator as expr_eval
from expression_type import CONSTANT
from return_type import ReturnType

class Constant(expr.Expression):
    _value = None

    def __init__(self, value):
        error = None
        super().__init__(CONSTANT,
            expr_eval.ExpressionEvaluator(CONSTANT, lambda expression, state, _: (expression.get_value(), error)))
        self.set_value(value)

    def get_value(self):
        return self._value

    def set_value(self, value):
        if isinstance(value, str):
            self.evaluator.return_type = ReturnType.String
        elif isinstance(value, bool):
            self.evaluator.return_type = ReturnType.Boolean
        elif isinstance(value, numbers.Number):
            self.evaluator.return_type = ReturnType.Number
        elif isinstance(value, list):
            self.evaluator.return_type = ReturnType.Array
        else:
            self.evaluator.return_type = ReturnType.Object

        self._value = value

    def deep_equals(self, other: expr.Expression) -> bool:
        equal: bool
        if (other is not None and other.expr_type != self.expr_type):
            equal = False
        else:
            other_val = Constant(other).get_value()
            equal = self.get_value() == other_val

        return equal

    #TODO: toString
    #TODO: reverseString
