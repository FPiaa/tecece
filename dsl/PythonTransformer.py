
import ast
from . import dsl;

class PythonTransformer(ast.NodeTransformer):
    ctx_functions = []

    def visit_ClassDef(self, node: ast.ClassDef):
        self.generic_visit(node)
        node.body = [*self.ctx_functions, *node.body]
        return node
    
    def visit_FunctionDef(self, node: ast.FunctionDef):
        precondition_found = [
            x
            for x in node.decorator_list
            if isinstance(x, ast.Call)
            and (
                (isinstance(x.func, ast.Name) and x.func.id == "pl")
                or (isinstance(x.func, ast.Attribute) and x.func.attr == "pl")
            )
        ]

        if not precondition_found:
            return node

        if not isinstance(precondition_found[0].args[0], ast.Constant):
            return node

        precondition = dsl.parse(precondition_found[0].args[0].value, node.name)
        # print(ast.dump(precondition[2], indent=4))
        # early return
        print(ast.dump(node))
        
        for x in node.decorator_list:
            if isinstance(x, ast.Call) and (isinstance(x.func, ast.Name) and x.func.id == 'pl' or isinstance(x.func, ast.Attribute) and x.func.attr == 'pl'):
                call = ast.Name(id=precondition[0][2].name, ctx=ast.Load())
                x.args = [precondition[0][0], precondition[0][1], call]
                node.args = ast.arguments(args=[ast.arg(arg='self'), *[ast.arg(arg=x) for x in precondition[1]]])
                self.ctx_functions.append(precondition[0][2])
        return self.generic_visit(node)
    
    def visit_UnaryOp(self, node: ast.UnaryOp):
        print("unary op")
        check_nested = isinstance(node.operand, ast.UnaryOp) and node.op == node.operand.op
        check_op = lambda x: isinstance(x, ast.Call) and (x.func.id == 'Belief' or x.func.id == 'Goal')
        check_args = lambda x: isinstance(x.args[0], ast.Constant)

        make_input_parser = lambda x: x.func.id[0] + " " + x.args[0].value
        new_call = ast.Call(
            func=ast.Attribute(
                value=ast.Name(id='self', ctx=ast.Load()),
                attr='get',
                ctx=ast.Load()),
                args=[],
                keywords=[]
        )
        if check_nested and check_op(node.operand.operand):
            if check_args(node.operand.operand) and check_op(node.operand.operand):
                knowledge = dsl.parse_structure(make_input_parser(node.operand.operand))
                knowledge.keywords = [ast.keyword(arg='instant', value=ast.Constant(value=True))]
                new_call.args = [knowledge]
                new_call.func.attr = "add" if isinstance(node.op, ast.UAdd) else "rm"
                return new_call

        elif check_op(node.operand):
            knowledge = dsl.parse_structure(make_input_parser(node.operand))
            knowledge.keywords = [ast.keyword(arg='instant', value=ast.Constant(value=False))]
            new_call.args = [knowledge]
            new_call.func.attr = "add" if isinstance(node.op, ast.UAdd) else "rm"
            return new_call
        else:
            print(node.op == ast.UAdd())
            return node

