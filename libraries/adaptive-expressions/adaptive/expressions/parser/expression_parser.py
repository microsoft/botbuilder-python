import sys
from antlr4 import *
from expression_antlr_lexer import expression_antlr_lexer
from expression_antlr_parser import expression_antlr_parser
from expression_antlr_parserVisitor import expression_antlr_parserVisitor

class ExpressionParser:
    def antlrParse(self, expression):
        inputStream = InputStream(expression)
        lexer = expression_antlr_lexer(inputStream)
        tokenStream = CommonTokenStream(lexer)
        parser = expression_antlr_parser(tokenStream)
        exp = parser.exp()

        expressionContext = None
        if exp is not None:
            expressionContext = exp.expression()

        return expressionContext
