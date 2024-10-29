from dsl.grammar.ExprParser import ExprParser
from .grammar.dslVisitor import DslVisitor
import ast


class DslTransformer(ExprVisitor):
    def visitStart_(self, ctx: ExprParser.Start_Context):
        return ast.Expr(value=self.visit(ctx.expr()))

    def visitMultExpr(self, ctx: ExprParser.MultExprContext):
        left = self.visit(ctx.expr(0))
        right = self.visit(ctx.expr(1))
        op = ctx.getChild(1).getText()
        if op == "*":
            return ast.BinOp(left=left, right=right, op=ast.Mult())
        if op == "/":
            return ast.BinOp(left=left, right=right, op=ast.Div())

    def visitAddExpr(self, ctx: ExprParser.AddExprContext):
        left = self.visit(ctx.expr(0))
        right = self.visit(ctx.expr(1))
        op = ctx.getChild(1).getText()
        if op == "+":
            return ast.BinOp(left=left, right=right, op=ast.Add())
        if op == "-":
            return ast.BinOp(left=left, right=right, op=ast.Sub())

    def visitCmpExpr(self, ctx: ExprParser.CmpExprContext):
        left = self.visit(ctx.expr(0))
        right = self.visit(ctx.expr(1))
        op = ctx.getChild(1).getText()
        if op == "<":
            return ast.Compare(left=left, comparators=[right], ops=[ast.Lt()])
        if op == "<=":
            return ast.Compare(left=left, comparators=[right], ops=[ast.LtE()])
        if op == ">":
            return ast.Compare(left=left, comparators=[right], ops=[ast.Gt()])
        if op == ">=":
            return ast.Compare(left=left, comparators=[right], ops=[ast.GtE()])

    def visitEqExpr(self, ctx: ExprParser.EqExprContext):
        left = self.visit(ctx.expr(0))
        right = self.visit(ctx.expr(1))
        op = ctx.getChild(1).getText()
        if op == "==":
            return ast.Compare(left=left, comparators=[right], ops=[ast.Eq()])
        if op == "!=":
            return ast.Compare(left=left, comparators=[right], ops=[ast.NotEq()])

    def visitAndExpr(self, ctx: ExprParser.AndExprContext):
        left = self.visit(ctx.expr(0))
        right = self.visit(ctx.expr(1))
        return ast.BoolOp(values=[left, right], op=ast.And())

    def visitOuExpr(self, ctx: ExprParser.OuExprContext):
        left = self(ctx.expr(0))
        right = self(ctx.expr(1))
        return ast.BoolOp(values=[left, right], op=ast.Or())

    def visitParenExpr(self, ctx: ExprParser.ParenExprContext):
        return self.visit(ctx.expr())

    def visitNum(self, ctx: ExprParser.NumContext):
        return ast.Constant(value=int(ctx.INT().getText()))

    def visitIdent(self, ctx: ExprParser.IdentContext):
        return ast.Name(id=ctx.IDENT().getText(), ctx=ast.Load())
