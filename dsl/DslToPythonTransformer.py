from .grammar.DslParser import DslParser
from .grammar.DslVisitor import DslVisitor
import ast


class DslTransformer(DslVisitor):

    def __init__(self, function_name):
        self.function_name = function_name
        self.symbol_list = []
        self.trigger_symbols = []
        self.in_for = False


    def _always_true_ctx(self):
        return ast.FunctionDef(
            name=self.function_name + '_ctx',
            args=ast.arguments(
                posonlyargs=[],
                args=[ast.arg(arg='self')],
                kwonlyargs=[],
                kw_defaults=[],
                defaults=[]),
            body=[
                ast.Return(
                    value=ast.List(elts=[], ctx=ast.Load()))],
            decorator_list=[],
            type_params=[])
    
    # Visit a parse tree produced by DslParser#plan.
    def visitPlan(self, ctx:DslParser.PlanContext):
        modifier_text = ''
        if(ctx.modifier() is None):
            modifier_text= 'gain'
        else:
            modifier_text = 'gain' if ctx.modifier().getText() == "+" else "lose"
        modifier = ast.Name(id=modifier_text, ctx=ast.Load())
        trigger = self.visit(ctx.trigger())

        context_function = self._always_true_ctx() if ctx.condition_list() is None else self.visit(ctx.condition_list())
        return (modifier, trigger, context_function)


    # Visit a parse tree produced by DslParser#belief.
    def visitBelief(self, ctx:DslParser.BeliefContext):
        name = ctx.IDENTIFIER().getText()
        structure = self.visit(ctx.structure()) if ctx.structure() is not None else []
        return ast.Call(
            func=ast.Name(id='Belief', ctx=ast.Load()), 
            args=[ast.Constant(value=name), *structure],
            keywords=[]
            )
        


    # Visit a parse tree produced by DslParser#goal.
    def visitGoal(self, ctx:DslParser.GoalContext):
        name = ctx.IDENTIFIER().getText()
        structure = self.visit(ctx.structure()) if ctx.structure() is not None else []
        return ast.Call(
            func=ast.Name(id='Goal', ctx=ast.Load()), 
            args=[ast.Constant(value=name), *structure],
            keywords=[])


    # Visit a parse tree produced by DslParser#structure.
    def visitStructure(self, ctx:DslParser.StructureContext):
        structure_elements = ctx.structure_elements()

        if(structure_elements is None):
            return [ast.List(elts=[], ctx=ast.Load())]
        
        elements =  self.visit(structure_elements)
        elements = [ast.Tuple(elts=elements, ctx=ast.Load())]

        if(ctx.source() is not None):
            elements.append(self.visit(ctx.source()))

        return elements


    # Visit a parse tree produced by DslParser#structure_elements.
    def visitStructure_elements(self, ctx:DslParser.Structure_elementsContext):
        params = []

        for element in ctx.elements():
            el = self.visit(element)
            if(isinstance(el, ast.Name) and el.id not in self.symbol_list):
                self.symbol_list.append(el.id)
                string = ast.Constant(value=el.id)
                params.append(string)
            else: 
                params.append(el)

        return params


    # Visit a parse tree produced by DslParser#source.
    def visitSource(self, ctx:DslParser.SourceContext):
        return ast.Constant(value=[ctx.IDENTIFIER().getText()])


    # Visit a parse tree produced by DslParser#exprElement.
    def visitExprElement(self, ctx:DslParser.ExprElementContext):
        return self.visit(ctx.log_expr())


    # Visit a parse tree produced by DslParser#anyElement.
    def visitAnyElement(self, ctx:DslParser.AnyElementContext):
        return ast.Name(id='any', ctx=ast.Load())


    # Visit a parse tree produced by DslParser#condition_list.
    def visitCondition_list(self, ctx:DslParser.Condition_listContext):
        body = []
        last_for = None
        for condition in ctx.condition():
            cond = self.visit(condition)
            if(last_for is not None):
                last_for.body.append(cond)

                if(isinstance(cond, ast.For)):
                    last_for = cond
            
            else:
                if(isinstance(cond, ast.For)):
                    last_for = cond
                body.append(cond)
        
        if(last_for is not None):
            last_for.body.append(ast.Return(value=ast.List(elts=[ast.Name(id=x) for x in self.symbol_list])))
            body.append(ast.Return(value=ast.Constant(value=None)))  
        else:
            body.append(ast.Return(value=ast.Tuple(elts=[ast.Name(id=x) for x in self.symbol_list])))        

        return ast.FunctionDef(
            name=self.function_name + '_ctx',
            args=ast.arguments(
                posonlyargs=[],
                args=[ast.arg(arg='self')],
                kwonlyargs=[],
                kw_defaults=[],
                defaults=[]
            ),
            body=body,
            decorator_list=[],
            type_params=[]
        )



    # Visit a parse tree produced by DslParser#knowledgeCondition.
    def visitKnowledgeCondition(self, ctx:DslParser.KnowledgeConditionContext):
        self.in_for = True
        
        knowledge = self.visit(ctx.knowledge())

        knowledge_args = knowledge.args[1:2]
        if(len(knowledge_args) == 0 or isinstance(knowledge_args, ast.Tuple) and len(knowledge_args.elts) == 0):
            knowledge_args = None
        else:
            knowledge_args = knowledge_args[0]
            knowledge_args = [x for x in enumerate(knowledge_args.elts)
                              if (isinstance(x[1], ast.Name) and x[1].id in self.symbol_list) or 
                              isinstance(x[1], ast.Constant) and x[1].value in self.symbol_list
                              ]
        
        ast_for = ast.For()
        ast_for.target = ast.Name(id='temp_var', ctx=ast.Store())
        ast_for.iter = ast.Call(
            func=ast.Attribute(
                value=ast.Name(id='self', ctx=ast.Load()),
                attr='get',
                ctx=ast.Load()),
                args=[knowledge],
                keywords=[]
        )
        ast_for.body = []
        ast_for.orelse = []
        if(knowledge_args is not None):
            ast_for.body.append( 
                ast.Assign(
                    targets=[
                        ast.Tuple(
                            elts=[ast.Name(id=x[1].id if isinstance(x[1], ast.Name) else x[1].value.replace('"','').replace("'", "")) for x in knowledge_args],
                            ctx=ast.Store()
                        )
                    ],
                    value=ast.Tuple(elts=[ast.Subscript(
                        value=ast.Name(id='temp_var', ctx=ast.Load()),
                        slice=ast.Constant(value=x[0]), 
                        ctx=ast.Load()) for x in knowledge_args]), ctx=ast.Load())
            )

        return ast_for


        
    # Visit a parse tree produced by DslParser#exprCondition.
    def visitExprCondition(self, ctx:DslParser.ExprConditionContext):
        expr = self.visit(ctx.log_expr())
        return ast.If(
            test=ast.UnaryOp(op=ast.Not(), operand=expr),
            body=[
                ast.Continue() if self.in_for else ast.Return(value=ast.Constant(value=None)),
            ],
            orelse=[],
        )


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
        operand = self.visit(ctx.log_expr())
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
                raise Exception(f"Operação inválida, visitRel_comparison, esperado =, !=, <, <=, >, >= encontrado '{op}'")
        
        if(isinstance(left, ast.Compare)):
            left.ops.append(new_op)
            left.comparators.append(right)
            return left
        else:
            return ast.Compare(left=left, ops=[new_op], comparators=[right])


    # Visit a parse tree produced by DslParser#unary_expr.
    def visitUnary_expr(self, ctx:DslParser.Unary_exprContext):
        unary_op = ctx.getChild(0)
        operand = ctx.arith_expr(0)
        if(unary_op == '+'):
            return ast.UnaryOp(op=ast.UAdd(), operand=operand)
        if(unary_op == '-'):
            return ast.UnaryOp(op=ast.USub(), operand=operand)

        raise Exception(f"Operação inválida, visitUnary_expr, esperado + ou - encontrado '{unary_op}'")

    # Visit a parse tree produced by DslParser#sum_expr.
    def visitSum_expr(self, ctx:DslParser.Sum_exprContext):
        left = self.visit(ctx.arith_expr(0))
        right = self.visit(ctx.arith_expr(1))
        op = ctx.getChild(1).getText()
        if(op == '+'):
            return ast.BinOp(left=left, right=right, op=ast.Add())
        if(op == '-'):
            return ast.BinOp(left=left, right=right, op=ast.Add())

        raise Exception(f"Operação inválida, visitSum_expr, esperado + ou - encontrado '{op}'")


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

        raise Exception(f"Operação inválida, visitMult_expr, esperado * ou / encontrado '{op}'")



    # Visit a parse tree produced by DslParser#primary_call.
    def visitPrimary_call(self, ctx:DslParser.Primary_callContext):
        func = self.visit(ctx.primary())
        args = []
        if(ctx.function_params() is not None): 
            args = self.visit(ctx.function_params())
            print(args)
        
        return ast.Call(func=func, args=args, keywords=[])

    # Visit a parse tree produced by DslParser#function_params.
    def visitFunction_params(self, ctx:DslParser.Function_paramsContext):
        args = []
        for param in ctx.log_expr():
            args.append(self.visit(param))
        return args

    # Visit a parse tree produced by DslParser#primary_path.
    def visitPrimary_path(self, ctx:DslParser.Primary_pathContext):
        attr = ctx.IDENTIFIER().getText()
        value = self.visit(ctx.primary())
        return ast.Attribute(value=value, attr=attr, ctx=ast.Load())


    # Visit a parse tree produced by DslParser#primary_walrus.
    def visitPrimary_walrus(self, ctx:DslParser.Primary_walrusContext):
        name = ctx.IDENTIFIER().getText()
        
        if(name not in self.symbol_list):
            self.symbol_list.append(name)
        
        value = self.visit(ctx.log_expr())
        return ast.NamedExpr(target=ast.Name(id=name, ctx=ast.Store()), value=value)


    # Visit a parse tree produced by DslParser#primary_index.
    def visitPrimary_index(self, ctx:DslParser.Primary_indexContext):
        value = self.visit(ctx.primary())
        slice = self.visit(ctx.log_expr())
        return ast.Subscript(value=value, slice=slice, ctx=ast.Load())



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
        id = ctx.IDENTIFIER().getText()

        return ast.Name(id=id, ctx=ast.Load())


    # Visit a parse tree produced by DslParser#atomBool.
    def visitAtomBool(self, ctx:DslParser.AtomBoolContext):
        print("visit atom bool")
        text_boolean = ctx.BOOLEAN().getText()
        boolean = True if text_boolean == 'True' else False
        return ast.Constant(value=boolean)


    # Visit a parse tree produced by DslParser#atomNone.
    def visitAtomNone(self, ctx:DslParser.AtomNoneContext):
        return ast.Constant(value=None)


    # Visit a parse tree produced by DslParser#atomStr.
    def visitAtomStr(self, ctx:DslParser.AtomStrContext):
        return ast.Constant(value=ctx.ESCAPED_STR().getText())


    # Visit a parse tree produced by DslParser#atomParen.
    def visitAtomParen(self, ctx:DslParser.AtomParenContext):
        return self.visit(ctx.log_expr())
