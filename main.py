from _ast import (
    Call,
    Expr,
    Module,
)
import astor
import ast
from typing import Any
from ast import (
    ImportFrom,
    Not,
    And,
    BinOp,
    BoolOp,
    Compare,
    If,
    Import,
    Lt,
    LtE,
    Mult,
    Name,
    FunctionDef,
    Return,
    UnaryOp,
    alias,
    arguments,
    arg,
    Load,
    Constant,
)

from dsl.dsl import parse


class DocstringTransformer(ast.NodeTransformer):
    def visit_Expr(self, node: Expr) -> Expr:
        if isinstance(node.value, ast.Constant) and isinstance(node.value.value, str):
            return ast.copy_location(
                ast.Expr(
                    value=ast.Call(
                        func=ast.Name(id="print", ctx=ast.Load()),
                        args=[node.value],
                        keywords=[],
                    )
                ),
                node,
            )

        return node


class PrintTransformer(ast.NodeTransformer):
    def visit_Call(self, node: Call) -> Any:
        if isinstance(node.func, ast.Name) and node.func.id == "print":
            node.args = [
                (
                    x
                    if not (isinstance(x, ast.Constant) and isinstance(x.value, str))
                    else ast.Constant(x.value.upper())
                )
                for x in node.args
            ]

        return node


class CreateFunctionTransformer(ast.NodeTransformer):
    def visit_Module(self, node: Module) -> Any:
        return ast.copy_location(
            ast.Module(
                body=[
                    *[x for x in node.body if not isinstance(x, ast.Expr)],
                    ast.FunctionDef(
                        name="example",
                        args=ast.arguments(
                            posonlyargs=[],
                            args=[],
                            kwonlyargs=[],
                            kw_defaults=[],
                            defaults=[],
                        ),
                        body=[x for x in node.body if isinstance(x, ast.Expr)],
                        decorator_list=[],
                        returns=None,
                    ),
                    ast.Expr(
                        value=ast.Call(
                            func=ast.Name(id="example", ctx=ast.Load()),
                            args=[],
                            keywords=[],
                        )
                    ),
                ]
            ),
            node,
        )


class DslToPython(ast.NodeTransformer):
    def visit_FunctionDef(self, node: ast.FunctionDef) -> Any:
        precondition_found = [
            x
            for x in node.decorator_list
            if isinstance(x, ast.Call)
            and (
                (isinstance(x.func, ast.Name) and x.func.id == "precondition")
                or (isinstance(x.func, ast.Attribute) and x.func.attr == "precondition")
            )
        ]

        if not precondition_found:
            return node
        node.decorator_list = [
            x
            for x in node.decorator_list
            if not (
                isinstance(x, ast.Call)
                and (
                    (isinstance(x.func, ast.Name) and x.func.id == "precondition")
                    or (
                        isinstance(x.func, ast.Attribute)
                        and x.func.attr == "precondition"
                    )
                )
            )
        ]

        if not isinstance(precondition_found[0].args[0], ast.Constant):
            return node

        precondition = parse(precondition_found[0].args[0].value)
        # early return
        ast_condition = ast.If(
            test=ast.UnaryOp(op=ast.Not(), operand=precondition),
            body=[
                ast.Expr(
                    value=ast.Call(
                        func=Name(id="print", ctx=Load()),
                        args=[
                            Constant(value="Condição false"),
                        ],
                        keywords=[],
                    )
                ),
                Return(Constant(value=False)),
            ],
            orelse=[],
        )
        node.body = [ast_condition, *node.body]
        return node


with open("example.py", "r") as f:
    tree = ast.parse(f.read())
    tree = DslToPython().visit(tree)
    tree = ast.fix_missing_locations(tree)
    with open("build.py", "w") as f:
        f.write(astor.to_source(tree))
    exec(compile(tree, "<ast>", mode="exec"))
    print()
