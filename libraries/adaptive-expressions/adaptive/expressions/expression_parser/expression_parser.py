import re
from antlr4 import InputStream
from antlr4 import CommonTokenStream
from antlr4 import TerminalNode
from ..expression_type import (
    SUBTRACT,
    ADD,
    ACCESSOR,
    ELEMENT,
    CREATEARRAY,
    JSON,
    SETPROPERTY,
    CONCAT,
)
from ..expression import Expression
from ..expression_evaluator import EvaluatorLookup
from ..expression_parser_interface import ExpresssionParserInterface
from ..constant import Constant
from .generated import expression_antlr_lexer
from .generated import expression_antlr_parser as ep_parser
from .generated import expression_antlr_parserVisitor
from .expression_parser_error_listener import ParseErrorListener


class ExpressionTransformer(expression_antlr_parserVisitor):
    escape_regex = r"\\[^\r\n]?"

    lookup_function: EvaluatorLookup

    def __init__(self, lookup: EvaluatorLookup):
        super().__init__()
        self.lookup_function = lookup

    def transform(self, ctx):
        return self.visit(ctx)

    def visitUnaryOpExp(self, ctx: ep_parser.UnaryOpExpContext) -> Expression:
        unary_operation_name = ctx.getChild(0).getText()
        operand = self.visit(ctx.expression())
        if unary_operation_name in (SUBTRACT, ADD):
            return self.make_expression(unary_operation_name, Constant(0), operand)

        return self.make_expression(unary_operation_name, operand)

    def visitBinaryOpExp(self, ctx: ep_parser.BinaryOpExpContext) -> Expression:
        binary_operation_name = ctx.getChild(1).getText()
        left = self.visit(ctx.expression(0))
        right = self.visit(ctx.expression(1))

        return self.make_expression(binary_operation_name, left, right)

    def visitFuncInvokeExp(self, ctx: ep_parser.FuncInvokeExpContext) -> Expression:
        parameters = self.process_args_list(ctx.argsList())

        # Remove the check to check primaryExpression is just an IDENTIFIER to support '.' in template name
        function_name = ctx.primaryExpression().getText()

        if ctx.NON() is not None:
            function_name += ctx.NON().getText()

        return self.make_expression(function_name, parameters)

    def visitIdAtom(self, ctx: ep_parser.IdAtomContext) -> Expression:
        result: Expression
        symbol = ctx.getText().lower()
        if symbol == "false":
            result = Constant(False)
        elif symbol == "true":
            result = Constant(True)
        elif symbol == "none":
            result = Constant(None)
        else:
            result = self.make_expression(ACCESSOR, Constant(symbol))

        return result

    def visitIndexAccessExp(self, ctx: ep_parser.IndexAccessExpContext) -> Expression:
        exp_property = self.visit(ctx.expression())
        instance = self.visit(ctx.primaryExpression())

        return self.make_expression(ELEMENT, instance, exp_property)

    def visitMemberAccessExp(self, ctx: ep_parser.MemberAccessExpContext) -> Expression:
        exp_property = ctx.IDENTIFIER().getText()
        instance = self.visit(ctx.primaryExpression())

        return self.make_expression(ACCESSOR, Constant(exp_property), instance)

    def visitNumericAtom(self, ctx: ep_parser.NumericAtomContext) -> Expression:
        try:
            int_number_value = int(ctx.getText())

            return Constant(int_number_value)
        except:
            try:
                float_number_value = float(ctx.getText())

                return Constant(float_number_value)
            except:
                raise Exception(ctx.getText() + " is not a number")

    def visitParenthesisExp(self, ctx: ep_parser.ParenthesisExpContext) -> Expression:
        return self.visit(ctx.expression())

    def visitArrayCreationExp(
        self, ctx: ep_parser.ArrayCreationExpContext
    ) -> Expression:
        parameters = self.process_args_list(ctx.argsList())

        return self.make_expression(CREATEARRAY, parameters)

    def visitStringAtom(self, ctx: ep_parser.StringAtomContext):
        text = ctx.getText()
        if text.startswith("'") and text.endswith("'"):
            text = re.sub(r"\\'", "'", text[1:-1])
        elif text.startswith('"') and text.endswith('"'):
            text = re.sub(r'\\"', '"', text[1:-1])
        else:
            raise Exception("Invalid string " + text)

        return Constant(self.eval_escape(text))

    def visitJsonCreationExp(self, ctx: ep_parser.JsonCreationExpContext) -> Expression:
        exp = self.make_expression(JSON, Constant("{}"))
        if ctx.keyValuePairList() is not None:
            for kv_pair in ctx.keyValuePairList().keyValuePair():
                key = ""
                key_node = kv_pair.key().getChild(0)
                if isinstance(key_node, TerminalNode):
                    if key_node.symbol.type == ep_parser.IDENTIFIER:
                        key = key_node.getText()
                    else:
                        key = key_node.getText()[1:-1]

                exp = self.make_expression(
                    SETPROPERTY, exp, Constant(key), self.visit(kv_pair.expression())
                )

        return exp

    def visitStringInterpolationAtom(
        self, ctx: ep_parser.StringInterpolationAtomContext
    ) -> Expression:
        children = []
        for node in ctx.stringInterpolation().children:
            if isinstance(node, TerminalNode):
                node_type = node.symbol.type
                if node_type == ep_parser.TEMPLATE:
                    expression_string = self.trim_expression(node.getText())
                    children.append(
                        Expression.parse(expression_string, self.lookup_function)
                    )

                if node_type == ep_parser.ESCAPE_CHARACTER:
                    children.append(
                        Constant(
                            self.eval_escape(
                                node.getText().replace("\\`", "`").replace("\\$", "$")
                            )
                        )
                    )
            else:
                text = self.eval_escape(node.getText())
                children.append(Constant(text))

        return self.make_expression(CONCAT, children)

    def defaultResult(self) -> Expression:
        return Constant("")

    def make_expression(self, function_type: str, *children) -> Expression:
        if len(children) > 0 and isinstance(children[0], list):
            children = children[0]

        if self.lookup_function(function_type) is None:
            raise Exception(
                function_type
                + " does not have an evaluator, it's not a built-in function or a custom function."
            )

        return Expression.make_expression(
            function_type, self.lookup_function(function_type), children
        )

    def process_args_list(self, ctx: ep_parser.ArgsListContext):
        result = []
        if ctx is None:
            return result

        for child in ctx.children:
            if isinstance(child, ep_parser.ExpLambdaContext):
                eval_param = self.make_expression(
                    ACCESSOR, Constant(child.IDENTIFIER().getText())
                )
                eval_fun = self.visit(child.expression())
                result.append(eval_param)
                result.append(eval_fun)
            elif isinstance(child, ep_parser.ExpressionContext):
                result.append(self.visit(child))

        return result

    def trim_expression(self, expression: str) -> str:
        result = expression.strip()
        if result.startswith("$"):
            result = result[1:]

        result = result.strip()

        if result.startswith("{") and result.endswith("}"):
            result = result[1:-1]

        return result.strip()

    def eval_escape(self, text: str) -> str:
        valid_characters_dict = {"\\r": "\r", "\\n": "\n", "\\t": "\t", "\\\\": "\\"}

        text = re.sub(
            self.escape_regex,
            lambda x: valid_characters_dict.get(x.group())
            if x.group() in valid_characters_dict
            else x.group(),
            text,
        )

        return text


class ExpressionParser(ExpresssionParserInterface):
    evaluator_lookup: EvaluatorLookup

    expression_dict = {}

    def __init__(self, lookup=None):
        self.evaluator_lookup = lookup if lookup is not None else Expression.lookup

    @staticmethod
    def antlr_parse(expression: str):
        if ExpressionParser.expression_dict.get(expression) is not None:
            return ExpressionParser.expression_dict.get(expression)

        input_stream = InputStream(expression)
        lexer = expression_antlr_lexer(input_stream)
        lexer.removeErrorListeners()
        token_stream = CommonTokenStream(lexer)
        parser = ep_parser(token_stream)
        parser.removeErrorListeners()
        parser.addErrorListener(ParseErrorListener())
        parser.buildParseTrees = True
        exp = parser.exp()
        expression_context = None
        if exp is not None:
            expression_context = exp.expression()

        ExpressionParser.expression_dict.update({expression: expression_context})

        return expression_context

    def parse(self, expression: str) -> object:
        if not expression:
            return Constant("")

        return ExpressionTransformer(self.evaluator_lookup).transform(
            ExpressionParser.antlr_parse(expression)
        )
