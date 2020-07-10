# Generated from ../expression_antlr_parser.g4 by ANTLR 4.8
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .expression_antlr_parser import expression_antlr_parser
else:
    from expression_antlr_parser import expression_antlr_parser

# This class defines a complete generic visitor for a parse tree produced by expression_antlr_parser.

class expression_antlr_parserVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by expression_antlr_parser#exp.
    def visitExp(self, ctx:expression_antlr_parser.ExpContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by expression_antlr_parser#unaryOpExp.
    def visitUnaryOpExp(self, ctx:expression_antlr_parser.UnaryOpExpContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by expression_antlr_parser#binaryOpExp.
    def visitBinaryOpExp(self, ctx:expression_antlr_parser.BinaryOpExpContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by expression_antlr_parser#primaryExp.
    def visitPrimaryExp(self, ctx:expression_antlr_parser.PrimaryExpContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by expression_antlr_parser#funcInvokeExp.
    def visitFuncInvokeExp(self, ctx:expression_antlr_parser.FuncInvokeExpContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by expression_antlr_parser#idAtom.
    def visitIdAtom(self, ctx:expression_antlr_parser.IdAtomContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by expression_antlr_parser#jsonCreationExp.
    def visitJsonCreationExp(self, ctx:expression_antlr_parser.JsonCreationExpContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by expression_antlr_parser#stringAtom.
    def visitStringAtom(self, ctx:expression_antlr_parser.StringAtomContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by expression_antlr_parser#indexAccessExp.
    def visitIndexAccessExp(self, ctx:expression_antlr_parser.IndexAccessExpContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by expression_antlr_parser#stringInterpolationAtom.
    def visitStringInterpolationAtom(self, ctx:expression_antlr_parser.StringInterpolationAtomContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by expression_antlr_parser#memberAccessExp.
    def visitMemberAccessExp(self, ctx:expression_antlr_parser.MemberAccessExpContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by expression_antlr_parser#parenthesisExp.
    def visitParenthesisExp(self, ctx:expression_antlr_parser.ParenthesisExpContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by expression_antlr_parser#numericAtom.
    def visitNumericAtom(self, ctx:expression_antlr_parser.NumericAtomContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by expression_antlr_parser#arrayCreationExp.
    def visitArrayCreationExp(self, ctx:expression_antlr_parser.ArrayCreationExpContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by expression_antlr_parser#stringInterpolation.
    def visitStringInterpolation(self, ctx:expression_antlr_parser.StringInterpolationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by expression_antlr_parser#textContent.
    def visitTextContent(self, ctx:expression_antlr_parser.TextContentContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by expression_antlr_parser#argsList.
    def visitArgsList(self, ctx:expression_antlr_parser.ArgsListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by expression_antlr_parser#expLambda.
    def visitExpLambda(self, ctx:expression_antlr_parser.ExpLambdaContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by expression_antlr_parser#keyValuePairList.
    def visitKeyValuePairList(self, ctx:expression_antlr_parser.KeyValuePairListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by expression_antlr_parser#keyValuePair.
    def visitKeyValuePair(self, ctx:expression_antlr_parser.KeyValuePairContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by expression_antlr_parser#key.
    def visitKey(self, ctx:expression_antlr_parser.KeyContext):
        return self.visitChildren(ctx)



del expression_antlr_parser