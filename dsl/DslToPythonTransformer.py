from .grammar.DslParser import DslParser
from .grammar.DslVisitor import DslVisitor
import ast


class DslTransformer(DslVisitor):
    # Visit a parse tree produced by DslParser#prog.
    def visitProg(self, ctx:DslParser.ProgContext):
        return self.visit(ctx.conditions())

    # Visit a parse tree produced by DslParser#function_params.
    def visitFunction_params(self, ctx:DslParser.Function_paramsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DslParser#conditions.
    def visitConditions(self, ctx:DslParser.ConditionsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DslParser#condition_list.
    def visitCondition_list(self, ctx:DslParser.Condition_listContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DslParser#condition.
    def visitCondition(self, ctx:DslParser.ConditionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DslParser#logical_or.
    def visitLogical_or(self, ctx:DslParser.Logical_orContext):
        left = self.visit(ctx.log_expr(0))
        right = self.visit(ctx.log_expr(1))
        return ast.BoolOp(values=[left, right], op=ast.Or())

    # Visit a parse tree produced by DslParser#logical_and.
    def visitLogical_and(self, ctx:DslParser.Logical_andContext):
        left = self.visit(ctx.log_expr(0))
        right = self.visit(ctx.log_expr(1))
        return ast.BoolOp(values=[left, right], op=ast.And())


    # Visit a parse tree produced by DslParser#logical_not.
    def visitLogical_not(self, ctx:DslParser.Logical_notContext):
        operand = self.visit(ctx.log_expr(0))
        return ast.UnaryOp(op=ast.Not(), operand=operand)

    # Visit a parse tree produced by DslParser#rel_comparison.
    def visitRel_comparison(self, ctx:DslParser.Rel_comparisonContext):
        left = self.visit(ctx.rel_expr(0))
        right = self.visit(ctx.rel_expr(1))
        op = ctx.getChild(1).getText()

        new_op = None
        match op:
            case'=':
                new_op = ast.Eq()
            case '!=':
                new_op = ast.NotEq()
            case '<':
                new_op = ast.Lt()
            case '<=':
                new_op = ast.LtE()
            case '>':
                new_op = ast.Gt()
            case '>=':
                new_op = ast.GtE()
            case _:
                raise Error(f"Operação inválida, visitRel_comparison, esperado =, !=, <, <=, >, >= encontrado '{op}'")
        
        if(isinstance(left, ast.Compare)):
            left.ops.append(op)
            left.comparators.append(right)
            return left
        else:
            ast.Compare(left=left, ops=[op], comparators=[right])


    # Visit a parse tree produced by DslParser#unary_expr.
    def visitUnary_expr(self, ctx:DslParser.Unary_exprContext):
        unary_op = ctx.getChild(0)
        operand = ctx.arith_expr(0)
        if(unary_op == '+'):
            return ast.UnaryOp(op=ast.UAdd(), operand=operand)
        if(unary_op == '*'):
            return ast.UnaryOp(op=ast.USub(), operand=operand)

        raise Error(f"Operação inválida, visitUnary_expr, esperado + ou - encontrado '{unary_op}'")

    # Visit a parse tree produced by DslParser#sum_expr.
    def visitSum_expr(self, ctx:DslParser.Sum_exprContext):
        left = self.visit(ctx.arith_expr(0))
        right = self.visit(ctx.arith_expr(1))
        op = ctx.getChild(1).getText()
        if(op == '+'):
            return ast.BinOp(left=left, right=right, op=ast.Add())
        if(op == '-'):
            return ast.BinOp(left=left, right=right, op=ast.Add())

        raise Error(f"Operação inválida, visitSum_expr, esperado + ou - encontrado '{op}'")


    # Visit a parse tree produced by DslParser#exp_expr.
    def visitExp_expr(self, ctx:DslParser.Exp_exprContext):
        base = self.visit(ctx.arith_expr(0))
        exponent = self.visit(ctx.arith_expr(1))
        return ast.BinOp(left=base, right=exponent, op=ast.Pow())


    # Visit a parse tree produced by DslParser#mult_expr.
    def visitMult_expr(self, ctx:DslParser.Mult_exprContext):
        left = self.visit(ctx.arith_expr(0))
        right = self.visit(ctx.arith_expr(1))
        op = ctx.getChild(1).getText()
        if op == "*":
            return ast.BinOp(left=left, right=right, op=ast.Mult())
        if op == "/":
            return ast.BinOp(left=left, right=right, op=ast.Div())
        if op == "%":
            return ast.BinOp(left=left, right=right, op=ast.Mod())

        raise Error(f"Operação inválida, visitMult_expr, esperado * ou / encontrado '{op}'")



    # Visit a parse tree produced by DslParser#primary_call.
    def visitPrimary_call(self, ctx:DslParser.Primary_callContext):
        func = self.visit(ctx.primary())
        args = []
        print(func)
        if(ctx.function_params() is not None): 
            args = self.visit(ctx.function_params())
            print(args)
        
        return ast.Call(func=func, args=args, keywords=[])


    # Visit a parse tree produced by DslParser#primary_path.
    def visitPrimary_path(self, ctx:DslParser.Primary_pathContext):
        attr = ctx.IDENTIFIER().getText()
        value = self.visit(ctx.primary())
        return ast.Attribute(value=value, attr=attr, ctx=ast.Load())


    # Visit a parse tree produced by DslParser#primary_walrus.
    def visitPrimary_walrus(self, ctx:DslParser.Primary_walrusContext):
        name = ctx.IDENTIFIER().getText()
        value = self.visit(ctx.log_expr())
        return ast.NamedExpr(target=ast.Name(id=name, ctx=ast.Store()), value=value)


    # Visit a parse tree produced by DslParser#primary_index.
    def visitPrimary_index(self, ctx:DslParser.Primary_indexContext):
        value = self.visit(ctx.primary())
        slice = self.visit(ctx.log_expr())
        return ast.Subscript(value=value, slice=slice, ctx=ast.Load())


    # Visit a parse tree produced by DslParser#atom.
    def visitAtom(self, ctx:DslParser.AtomContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DslParser#tuple.
    def visitTuple(self, ctx:DslParser.TupleContext):
        params = self.visit(ctx.tuple_params())
        return ast.Tuple(elts=params, ctx=ast.Load())
    
    def visitTuple_params(self, ctx:DslParser.Tuple_paramsContext):
        params = []
        for el in ctx.log_expr():
            params.append(self.visit(el))
        return params

    # Visit a parse tree produced by DslParser#array.
    def visitArray(self, ctx:DslParser.ArrayContext):
        params = self.visit(ctx.array_params())
        return ast.List(elts=params, ctx=ast.Load())

    # Visit a parse tree produced by DslParser#array_params.
    def visitArray_params(self, ctx:DslParser.Array_paramsContext):
        params = []
        for el in ctx.log_expr():
            params.append(self.visit(el))
        return params


    # Visit a parse tree produced by DslParser#dict.
    def visitDict(self, ctx:DslParser.DictContext):
        elements = self.visit(ctx.dict_params())
        keys = [x[0] for x in elements]
        values = [x[1] for x in elements]
        return ast.Dict(keys=keys, values=values)

    # Visit a parse tree produced by DslParser#dict_params.
    def visitDict_params(self, ctx:DslParser.Dict_paramsContext):
        params = []
        for pair in ctx.dict_pair():
            params.append(self.visit(pair))
        return params

    # Visit a parse tree produced by DslParser#dict_pair.
    def visitDict_pair(self, ctx:DslParser.Dict_pairContext):
        key = self.visit(ctx.log_expr(0))
        value = self.visit(ctx.log_expr(1))
        return (key, value)

    # Visit a parse tree produced by DslParser#atomNumber.
    def visitAtomNumber(self, ctx:DslParser.AtomNumberContext):
        return ast.Constant(value=int(ctx.NUMBER().getText()))


    # Visit a parse tree produced by DslParser#atomIdent.
    def visitAtomIdent(self, ctx:DslParser.AtomIdentContext):
        return ast.Name(id=ctx.IDENTIFIER().getText(), ctx=ast.Load())


    # Visit a parse tree produced by DslParser#atomBool.
    def visitAtomBool(self, ctx:DslParser.AtomBoolContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DslParser#atomNone.
    def visitAtomNone(self, ctx:DslParser.AtomNoneContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DslParser#atomTuple.
    def visitAtomTuple(self, ctx:DslParser.AtomTupleContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DslParser#atomArray.
    def visitAtomArray(self, ctx:DslParser.AtomArrayContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DslParser#atomDict.
    def visitAtomDict(self, ctx:DslParser.AtomDictContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DslParser#atomParen.
    def visitAtomParen(self, ctx:DslParser.AtomParenContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DslParser#atomStr.
    def visitAtomStr(self, ctx:DslParser.AtomStrContext):
        return self.visitChildren(ctx)
