# Generated from ../expression_antlr_parser.g4 by ANTLR 4.8
from antlr4 import *

if __name__ is not None and "." in __name__:
    from .expression_antlr_parser import expression_antlr_parser
else:
    from expression_antlr_parser import expression_antlr_parser

# This class defines a complete listener for a parse tree produced by expression_antlr_parser.
class expression_antlr_parserListener(ParseTreeListener):

    # Enter a parse tree produced by expression_antlr_parser#exp.
    def enterExp(self, ctx: expression_antlr_parser.ExpContext):
        pass

    # Exit a parse tree produced by expression_antlr_parser#exp.
    def exitExp(self, ctx: expression_antlr_parser.ExpContext):
        pass

    # Enter a parse tree produced by expression_antlr_parser#unaryOpExp.
    def enterUnaryOpExp(self, ctx: expression_antlr_parser.UnaryOpExpContext):
        pass

    # Exit a parse tree produced by expression_antlr_parser#unaryOpExp.
    def exitUnaryOpExp(self, ctx: expression_antlr_parser.UnaryOpExpContext):
        pass

    # Enter a parse tree produced by expression_antlr_parser#binaryOpExp.
    def enterBinaryOpExp(self, ctx: expression_antlr_parser.BinaryOpExpContext):
        pass

    # Exit a parse tree produced by expression_antlr_parser#binaryOpExp.
    def exitBinaryOpExp(self, ctx: expression_antlr_parser.BinaryOpExpContext):
        pass

    # Enter a parse tree produced by expression_antlr_parser#primaryExp.
    def enterPrimaryExp(self, ctx: expression_antlr_parser.PrimaryExpContext):
        pass

    # Exit a parse tree produced by expression_antlr_parser#primaryExp.
    def exitPrimaryExp(self, ctx: expression_antlr_parser.PrimaryExpContext):
        pass

    # Enter a parse tree produced by expression_antlr_parser#funcInvokeExp.
    def enterFuncInvokeExp(self, ctx: expression_antlr_parser.FuncInvokeExpContext):
        pass

    # Exit a parse tree produced by expression_antlr_parser#funcInvokeExp.
    def exitFuncInvokeExp(self, ctx: expression_antlr_parser.FuncInvokeExpContext):
        pass

    # Enter a parse tree produced by expression_antlr_parser#idAtom.
    def enterIdAtom(self, ctx: expression_antlr_parser.IdAtomContext):
        pass

    # Exit a parse tree produced by expression_antlr_parser#idAtom.
    def exitIdAtom(self, ctx: expression_antlr_parser.IdAtomContext):
        pass

    # Enter a parse tree produced by expression_antlr_parser#jsonCreationExp.
    def enterJsonCreationExp(self, ctx: expression_antlr_parser.JsonCreationExpContext):
        pass

    # Exit a parse tree produced by expression_antlr_parser#jsonCreationExp.
    def exitJsonCreationExp(self, ctx: expression_antlr_parser.JsonCreationExpContext):
        pass

    # Enter a parse tree produced by expression_antlr_parser#stringAtom.
    def enterStringAtom(self, ctx: expression_antlr_parser.StringAtomContext):
        pass

    # Exit a parse tree produced by expression_antlr_parser#stringAtom.
    def exitStringAtom(self, ctx: expression_antlr_parser.StringAtomContext):
        pass

    # Enter a parse tree produced by expression_antlr_parser#indexAccessExp.
    def enterIndexAccessExp(self, ctx: expression_antlr_parser.IndexAccessExpContext):
        pass

    # Exit a parse tree produced by expression_antlr_parser#indexAccessExp.
    def exitIndexAccessExp(self, ctx: expression_antlr_parser.IndexAccessExpContext):
        pass

    # Enter a parse tree produced by expression_antlr_parser#stringInterpolationAtom.
    def enterStringInterpolationAtom(
        self, ctx: expression_antlr_parser.StringInterpolationAtomContext
    ):
        pass

    # Exit a parse tree produced by expression_antlr_parser#stringInterpolationAtom.
    def exitStringInterpolationAtom(
        self, ctx: expression_antlr_parser.StringInterpolationAtomContext
    ):
        pass

    # Enter a parse tree produced by expression_antlr_parser#memberAccessExp.
    def enterMemberAccessExp(self, ctx: expression_antlr_parser.MemberAccessExpContext):
        pass

    # Exit a parse tree produced by expression_antlr_parser#memberAccessExp.
    def exitMemberAccessExp(self, ctx: expression_antlr_parser.MemberAccessExpContext):
        pass

    # Enter a parse tree produced by expression_antlr_parser#parenthesisExp.
    def enterParenthesisExp(self, ctx: expression_antlr_parser.ParenthesisExpContext):
        pass

    # Exit a parse tree produced by expression_antlr_parser#parenthesisExp.
    def exitParenthesisExp(self, ctx: expression_antlr_parser.ParenthesisExpContext):
        pass

    # Enter a parse tree produced by expression_antlr_parser#numericAtom.
    def enterNumericAtom(self, ctx: expression_antlr_parser.NumericAtomContext):
        pass

    # Exit a parse tree produced by expression_antlr_parser#numericAtom.
    def exitNumericAtom(self, ctx: expression_antlr_parser.NumericAtomContext):
        pass

    # Enter a parse tree produced by expression_antlr_parser#arrayCreationExp.
    def enterArrayCreationExp(
        self, ctx: expression_antlr_parser.ArrayCreationExpContext
    ):
        pass

    # Exit a parse tree produced by expression_antlr_parser#arrayCreationExp.
    def exitArrayCreationExp(
        self, ctx: expression_antlr_parser.ArrayCreationExpContext
    ):
        pass

    # Enter a parse tree produced by expression_antlr_parser#stringInterpolation.
    def enterStringInterpolation(
        self, ctx: expression_antlr_parser.StringInterpolationContext
    ):
        pass

    # Exit a parse tree produced by expression_antlr_parser#stringInterpolation.
    def exitStringInterpolation(
        self, ctx: expression_antlr_parser.StringInterpolationContext
    ):
        pass

    # Enter a parse tree produced by expression_antlr_parser#textContent.
    def enterTextContent(self, ctx: expression_antlr_parser.TextContentContext):
        pass

    # Exit a parse tree produced by expression_antlr_parser#textContent.
    def exitTextContent(self, ctx: expression_antlr_parser.TextContentContext):
        pass

    # Enter a parse tree produced by expression_antlr_parser#argsList.
    def enterArgsList(self, ctx: expression_antlr_parser.ArgsListContext):
        pass

    # Exit a parse tree produced by expression_antlr_parser#argsList.
    def exitArgsList(self, ctx: expression_antlr_parser.ArgsListContext):
        pass

    # Enter a parse tree produced by expression_antlr_parser#expLambda.
    def enterExpLambda(self, ctx: expression_antlr_parser.ExpLambdaContext):
        pass

    # Exit a parse tree produced by expression_antlr_parser#expLambda.
    def exitExpLambda(self, ctx: expression_antlr_parser.ExpLambdaContext):
        pass

    # Enter a parse tree produced by expression_antlr_parser#keyValuePairList.
    def enterKeyValuePairList(
        self, ctx: expression_antlr_parser.KeyValuePairListContext
    ):
        pass

    # Exit a parse tree produced by expression_antlr_parser#keyValuePairList.
    def exitKeyValuePairList(
        self, ctx: expression_antlr_parser.KeyValuePairListContext
    ):
        pass

    # Enter a parse tree produced by expression_antlr_parser#keyValuePair.
    def enterKeyValuePair(self, ctx: expression_antlr_parser.KeyValuePairContext):
        pass

    # Exit a parse tree produced by expression_antlr_parser#keyValuePair.
    def exitKeyValuePair(self, ctx: expression_antlr_parser.KeyValuePairContext):
        pass

    # Enter a parse tree produced by expression_antlr_parser#key.
    def enterKey(self, ctx: expression_antlr_parser.KeyContext):
        pass

    # Exit a parse tree produced by expression_antlr_parser#key.
    def exitKey(self, ctx: expression_antlr_parser.KeyContext):
        pass


del expression_antlr_parser
