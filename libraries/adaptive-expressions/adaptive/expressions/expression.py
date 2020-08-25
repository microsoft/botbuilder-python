from typing import Callable
from .expression_evaluator import ExpressionEvaluator, EvaluateExpressionDelegate
from .memory_interface import MemoryInterface
from .memory.simple_object_memory import SimpleObjectMemory
from .extensions import Extensions
from .options import Options
from .expression_type import (
    AND,
    OR,
    ACCESSOR,
    ELEMENT,
    FOREACH,
    WHERE,
    SELECT,
    EQUAL,
    NOT,
    LAMBDA,
    SETPATHTOVALUE,
)
from .function_table import FunctionTable
from .return_type import ReturnType

# pylint: disable=import-outside-toplevel
class Expression:
    evaluator: ExpressionEvaluator
    children = []
    functions = {}
    functions = FunctionTable()

    def __init__(self, expr_type: str, evaluator: ExpressionEvaluator, children=None):
        if evaluator is not None:
            self.evaluator = evaluator
            self.children = children if children is not None else []
        elif expr_type is not None:
            if self.functions.get(expr_type) is None:
                raise Exception(
                    expr_type
                    + " does not have an evaluator, it's not a built-in function or a custom function."
                )

            self.evaluator = self.functions.get(expr_type)
            self.children = children if children is not None else []

    @property
    def return_type(self):
        return self.evaluator.return_type

    @property
    def expr_type(self):
        return self.evaluator.expr_type

    def deep_equals(self, other: object) -> bool:
        if other is None:
            return False

        if self.expr_type != other.expr_type:
            return False

        equal = len(self.children) == len(other.children)
        if self.expr_type == AND or self.expr_type == OR:
            index = 0
            while equal and index < len(self.children):
                primary = self.children[0]
                found = False
                for j in range(len(self.children)):
                    if primary.deep_equals(other.children[j]):
                        found = True
                        break

                equal = found
                index = index + 1
        else:
            index = 0
            while equal and index < len(self.children):
                equal = self.children[index].deep_equals(other.children[index])
                index = index + 1

        return equal

    def references(self):
        path, refs = self.reference_walk(self)
        if path is not None:
            refs.add(path)

        return list(refs)

    # pylint: disable=too-many-statements
    def reference_walk(
        self, expression: object, extension: Callable[[object], bool] = None
    ):
        from .constant import Constant

        path: str
        refs = set()
        if extension is None or extension(expression):
            children = expression.children
            if expression.expr_type == ACCESSOR:
                prop = str(Constant(children[0]).get_value())

                if len(children) == 1:
                    path = prop

                if len(children) == 2:
                    path, refs = self.reference_walk(children[1], extension)
                    if path is not None:
                        path = path + "." + prop
            elif expression.expr_type == ELEMENT:
                path, refs = self.reference_walk(children[0], extension)
                if path is not None:
                    if isinstance(children[1], Constant):
                        cnst = Constant(children[1])
                        if cnst.return_type == ReturnType.String:
                            path += "." + cnst.get_value()
                        else:
                            path += "[" + cnst.get_value + "]"
                    else:
                        refs.add(path)

                result = self.reference_walk(children[1], extension)
                idx_path = result[0]
                refs1 = result[1]
                refs = refs.union(refs1)
                if idx_path is not None:
                    refs.add(idx_path)
            elif (
                expression.expr_type == FOREACH
                or expression.expr_type == WHERE
                or expression.expr_type == SELECT
            ):
                result = self.reference_walk(children[0], extension)
                child0_path = result[0]
                refs0 = result[1]
                if child0_path is not None:
                    refs0.add(child0_path)

                result = self.reference_walk(children[2], extension)
                child2_path = result[0]
                refs2 = result[1]
                if child2_path is not None:
                    refs2.add(child2_path)

                iterator_name = str(Constant(children[1].children[0]).get_value())
                non_local_refs = list(
                    filter(
                        lambda x: (
                            x == iterator_name
                            or x.startswith(iterator_name + ".")
                            or x.startswith(iterator_name + "[")
                        ),
                        refs2,
                    )
                )
                refs = refs.union(refs0, non_local_refs)
            else:
                for child in expression.children:
                    result = self.reference_walk(child, extension)
                    child_path = result[0]
                    refs0 = result[1]
                    refs = refs.union(refs0)
                    if child_path is not None:
                        refs.add(child_path)

        return path, refs

    @staticmethod
    def parse(expression: str, lookup=None):
        from .expression_parser import ExpressionParser

        return ExpressionParser(
            lookup if lookup is not None else Expression.lookup
        ).parse(expression)

    @staticmethod
    def lookup(function_name: str) -> ExpressionEvaluator:
        expr_evaluator = Expression.functions.get(function_name)
        if expr_evaluator is None:
            return None

        return expr_evaluator

    @staticmethod
    def make_expression(exp_type: str, evaluator: ExpressionEvaluator, children: list):
        expr = Expression(exp_type, evaluator, children)
        expr.validate()

        return expr

    @staticmethod
    def lambda_expression(func: EvaluateExpressionDelegate):
        return Expression(LAMBDA, ExpressionEvaluator(LAMBDA, func))

    @staticmethod
    def lambda_func(func: object):
        def anonymous_function(_expression: object, state: object, _: Options):
            value: object = None
            error: str = None
            try:
                value = func(state)
            except Exception as err:
                error = str(err)

            return value, error

        return Expression(LAMBDA, ExpressionEvaluator(LAMBDA, anonymous_function))

    @staticmethod
    def set_path_to_value(property: object, value: object):
        from .constant import Constant

        if isinstance(value, Expression):
            return Expression.make_expression(SETPATHTOVALUE, None, property, value)

        return Expression.make_expression(
            SETPATHTOVALUE, None, property, Constant(value)
        )

    @staticmethod
    def equals_expression(children: list):
        return Expression.make_expression(EQUAL, None, children)

    @staticmethod
    def and_expression(children: list):
        if len(children) > 1:
            return Expression.make_expression(AND, None, children)

        return children[0]

    @staticmethod
    def or_expression(children: list):
        if len(children) > 1:
            return Expression.make_expression(OR, None, children)

        return children[0]

    @staticmethod
    def not_expression(child: object):
        return Expression.make_expression(NOT, None, child)

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

    def to_string(self):
        from .constant import Constant

        builder = ""
        valid = False
        # Special support for memory paths
        if self.expr_type == ACCESSOR and len(self.children) >= 1:
            # pylint: disable=line-too-long
            if isinstance(self.children[0], Constant) and isinstance(
                Constant(self.children[0]).get_value(), str
            ):
                prop = self.children[0].get_value()
                if len(self.children) == 1:
                    valid = True
                    builder += prop
                elif len(self.children) == 2:
                    valid = True
                    builder += self.children[1].to_string()
                    builder += "."
                    builder += prop
        elif self.expr_type == ELEMENT and len(self.children) == 2:
            valid = True
            builder += self.children[0].to_string()
            builder += "["
            builder += self.children[1].to_string()
            builder += "]"

        if valid is False:
            infix = (
                len(self.expr_type) > 0
                and not self.expr_type[0].isalpha()
                and len(self.children) >= 2
            )
            if infix is False:
                builder += self.expr_type
            builder += "("
            first = True
            for child in self.children:
                if first:
                    first = False
                else:
                    if infix:
                        builder += " "
                        builder += self.expr_type
                        builder += " "
                    else:
                        builder += ", "
                builder += child.to_string()
            builder += ")"
        return builder
