from dsl.grammar.DslParser import DslParser
from .grammar.DslVisitor import DslVisitor
import ast


class DslTransformer(DslVisitor):
    # Visit a parse tree produced by DslParser#prog.
    def visitProg(self, ctx:DslParser.ProgContext):
        if(ctx.conditions):
            self.visit(ctx.conditions)
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DslParser#knowledge.
    def visitKnowledge(self, ctx:DslParser.KnowledgeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DslParser#use.
    def visitUse(self, ctx:DslParser.UseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DslParser#belief.
    def visitBelief(self, ctx:DslParser.BeliefContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DslParser#goal.
    def visitGoal(self, ctx:DslParser.GoalContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DslParser#modifier.
    def visitModifier(self, ctx:DslParser.ModifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DslParser#structure.
    def visitStructure(self, ctx:DslParser.StructureContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DslParser#structure_elements.
    def visitStructure_elements(self, ctx:DslParser.Structure_elementsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DslParser#source.
    def visitSource(self, ctx:DslParser.SourceContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DslParser#elements.
    def visitElements(self, ctx:DslParser.ElementsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DslParser#bind.
    def visitBind(self, ctx:DslParser.BindContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DslParser#function_call.
    def visitFunction_call(self, ctx:DslParser.Function_callContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DslParser#function_path.
    def visitFunction_path(self, ctx:DslParser.Function_pathContext):
        return self.visitChildren(ctx)


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


    # Visit a parse tree produced by DslParser#pattern_match_expr.
    def visitPattern_match_expr(self, ctx:DslParser.Pattern_match_exprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DslParser#pattern_match_tuple.
    def visitPattern_match_tuple(self, ctx:DslParser.Pattern_match_tupleContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DslParser#pattern.
    def visitPattern(self, ctx:DslParser.PatternContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DslParser#array_pattern.
    def visitArray_pattern(self, ctx:DslParser.Array_patternContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DslParser#range_pattern.
    def visitRange_pattern(self, ctx:DslParser.Range_patternContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DslParser#inclusive_range_pattern.
    def visitInclusive_range_pattern(self, ctx:DslParser.Inclusive_range_patternContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DslParser#tuple.
    def visitTuple(self, ctx:DslParser.TupleContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DslParser#tuple_params.
    def visitTuple_params(self, ctx:DslParser.Tuple_paramsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DslParser#tuple_pattern.
    def visitTuple_pattern(self, ctx:DslParser.Tuple_patternContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DslParser#tuple_pattern_params.
    def visitTuple_pattern_params(self, ctx:DslParser.Tuple_pattern_paramsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DslParser#log_expr.
    def visitLog_expr(self, ctx:DslParser.Log_exprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DslParser#rel_expr.
    def visitRel_expr(self, ctx:DslParser.Rel_exprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DslParser#arith_expr.
    def visitArith_expr(self, ctx:DslParser.Arith_exprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by DslParser#expr.
    def visitExpr(self, ctx:DslParser.ExprContext):
        return self.visitChildren(ctx)
