import enum

from expression_parser import ExpressionParser
from memory import MemoryInterface, SimpleObjectMemory
from .extensions import Extensions
from .options import Options
from .expression_evaluator import ExpressionEvaluator

class ReturnType(enum.Enum):
    "True or false boolean value."
    Boolean = 1,

    "Numerical value like int, float, double, ..."
    Number = 2,

    "Any value is possible."
    Object = 4,

    "String value."
    String = 8,

    "Array value."
    Array = 16

class Expression():
    evaluator: ExpressionEvaluator
    children = []
    functions = {}

    def __init__(self, expr_type: str, evaluator: ExpressionEvaluator, children=None):
        if evaluator is not None:
            self.evaluator = evaluator
            self.children = children if children is not None else []
        elif expr_type is not None:
            if self.functions.get(expr_type) is None:
                raise Exception(expr_type
                    + ' does not have an evaluator, it\'s not a built-in function or a custom function.')

            self.evaluator = self.functions.get(expr_type)
            self.children = children if children is not None else []

    @property
    def return_type(self):
        return self.evaluator.return_type

    @property
    def expr_type(self):
        return self.evaluator.expr_type

    #TODO: deepEquals

    #TODO: references

    #TODO: referenceWalk

    @staticmethod
    def parse(expression: str, lookup=None):
        return ExpressionParser(lookup if lookup is not None else Expression.lookup).parse(expression)

    @staticmethod
    def lookup(function_name: str) -> ExpressionEvaluator:
        expr_evaluator = Expression.functions.get(function_name)
        if expr_evaluator is None:
            return None

        return expr_evaluator

    @staticmethod
    def make_expression(exp_type: str, evaluator: ExpressionEvaluator, children: list) -> Expression:
        expr = Expression(exp_type, evaluator, children)
        expr.validate()

        return expr

    #TODO: lambaExpression
    #TODO: lamba
    #TODO: setPathToValue
    #TODO: equalsExpression
    #TODO: andExpression
    #TODO: orExpression
    #TODO: notExpression

    def validate(self):
        self.evaluator.validate_expression(self)

    def validate_tree(self):
        self.validate()
        for child in self.children:
            child.validate_tree()

    def try_evaluate(self, state: MemoryInterface, options: Options = None):
        if Extensions.is_memeory_interface(state) is False:
            state = SimpleObjectMemory.wrap(state)

        if options is None:
            options = Options()

        return self.evaluator.try_evaluate(self, state, options)

    #TODO: toString
