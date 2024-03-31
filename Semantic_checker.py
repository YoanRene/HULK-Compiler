from Automata import *
from Grammar import *
from Parser import *
from ParserLR1 import *
from Regex import *
import Visitor as visitor
import itertools as itl

def evaluate_reverse_parse(right_parse, operations, tokens):
    if not right_parse or not operations or not tokens:
        return

    right_parse = iter(right_parse)
    tokens = iter(tokens)
    stack = []
    for operation in operations:
        if operation == ShiftReduceParser.SHIFT:
            token = next(tokens)
            stack.append(token.lex)
        elif operation == ShiftReduceParser.REDUCE:
            production = next(right_parse)
            head, body = production
            attributes = production.attributes
            assert all(rule is None for rule in attributes[1:]), 'There must be only synteticed attributes.'
            rule = attributes[0]

            if len(body):
                synteticed = [None] + stack[-len(body):]
                value = rule(None, synteticed)
                stack[-len(body):] = [value]
            else:
                stack.append(rule(None, None))
        else:
            raise Exception('Invalid action!!!')

    assert len(stack) == 1
    assert isinstance(next(tokens).token_type, EOF)
    return stack[0]

#region clases node
class Node:
    pass

class ProgramNode(Node):
    def __init__(self, statements,expr):
        self.statements = statements
        self.expr = expr
        
class StatementNode(Node):
    pass
        
class ExpressionNode(Node):
    pass

class VarDeclarationNode(StatementNode): #let
    def __init__(self, idx, expr):
        self.id = idx
        self.expr = expr

class FuncDeclarationNode(StatementNode):
    def __init__(self, idx, expr_list, expr):
        self.id = idx
        self.expr_list = expr_list
        self.expr = expr

class PrintNode(StatementNode):
    def __init__(self, expr):
        self.expr = expr

class AtomicNode(ExpressionNode):
    def __init__(self, lex):
        self.lex = lex

class BinaryNode(ExpressionNode):
    def __init__(self, left, right):
        self.left = left
        self.right = right

class ConstantNumNode(AtomicNode):
    def evaluate(self):
        return float(self.lex)

class VariableNode(AtomicNode):
    def evaluate(self):
        # Aquí implementa la lógica para obtener el valor de la variable
        pass

class CallNode(AtomicNode):
    def __init__(self, idx, args):
        AtomicNode.__init__(self, idx)
        self.args = args

class PlusNode(BinaryNode):
    def evaluate(self):
        return self.left.evaluate() + self.right.evaluate()

class MinusNode(BinaryNode):
    def evaluate(self):
        return self.left.evaluate() - self.right.evaluate()

class StarNode(BinaryNode):
    def evaluate(self):
        return self.left.evaluate() * self.right.evaluate()

class DivNode(BinaryNode):
    def evaluate(self):
        return self.left.evaluate() / self.right.evaluate()

class WhileNode(ExpressionNode):
    def __init__(self,boolean_expr,body):
        self.boolean_expr = boolean_expr
        self.body = body
        


class ForNode(ExpressionNode):
    def __init__(self,boolean_expr,iterable,body):
        self.boolean_expr = boolean_expr
        self.iterable = iterable
        self.body = body

class IfNode(ExpressionNode):
    def __init__(self,boolean_expr,expr,block_expr):
        pass

class ElseNode(ExpressionNode):
    def __init__(self,expr,block_expr):
        pass

class Conditional_expr(ExpressionNode):
    def __init__(self,if_expr,boolean_expr,expr,else_expr):
        pass

class Boolean_expr(ExpressionNode):
    def __init__(self,boolean_expr,comp_op,boolean_term):
        pass

class ModNode(BinaryNode):
    def evaluate(self):
        return self.left.evaluate() % self.right.evaluate()
    
class PowNode(BinaryNode):
    def evaluate(self):
        return self.left.evaluate() ** self.right.evaluate()
    
class ProtocolNode(ExpressionNode):
    def __init__(self, id, expr_list):
        self.id = id
        self.expr_list = expr_list

class MethodNode(ExpressionNode):
    def __init__(self, id, expr_list,id_ext):
        self.id = id
        self.expr_list = expr_list
        self.id_ext = id_ext

class DestructNode(ExpressionNode):
    def __init__(self, id, expr_list):
        self.id = id
        self.expr_list = expr_list

class AssignNode(ExpressionNode):
    def __init__(self, id, expr):
        self.id = id
        self.expr = expr

class Comparable_expression(ExpressionNode):
    def __init__(self,numerical_expr,string_expr):
        pass

class WhileNode(ExpressionNode):
    def __init__(self,condition,body):
        pass

class ForNode(ExpressionNode):
    def __init__(self,condition,body):
        pass

class BlockNode(ExpressionNode):
    def __init__(self,expr_list):
        pass

class TypePropCallNode(AtomicNode):
    def __init__(self, id,params):
        pass

class UnaryNode(ExpressionNode):
    def __init__(self,expr):
        self.expr= expr

class UnaryNumOpNode(UnaryNode):
    pass

class UnaryLogOpNode(UnaryNode):
    pass

class SqrtNode(UnaryNumOpNode):
    pass

class SinNode(UnaryNumOpNode):
    pass

class CosNode(UnaryNumOpNode):
    pass

class ExpNode(UnaryNumOpNode):
    pass

class NotNode(UnaryLogOpNode):
    pass

class PowNode(BinaryNode):
    pass

class LogNode(BinaryNode):
    pass

class AndNode(BinaryNode):
    pass

class OrNode(BinaryNode):
    pass

class ConcatNode(BinaryNode): ##
    pass 

#endregion

class FormatVisitor(object):
    @visitor.on('node')
    def visit(self, node, tabs):
        pass
    
    @visitor.when(ProgramNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\__ProgramNode [<stat>; ... <stat>;]'
        statements = '\n'.join(self.visit(child, tabs + 1) for child in node.statements)
        return f'{ans}\n{statements}'
    
    @visitor.when(PrintNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\__PrintNode <expr>'
        expr = self.visit(node.expr, tabs + 1)
        return f'{ans}\n{expr}'
    
    @visitor.when(VarDeclarationNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\__VarDeclarationNode: let {node.id} = <expr>'
        expr = self.visit(node.expr, tabs + 1)
        return f'{ans}\n{expr}'
    
    @visitor.when(FuncDeclarationNode)
    def visit(self, node, tabs=0):
        params = ', '.join(node.params)
        ans = '\t' * tabs + f'\\__FuncDeclarationNode: def {node.id}({params}) -> <expr>'
        body = self.visit(node.body, tabs + 1)
        return f'{ans}\n{body}'

    @visitor.when(BinaryNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\__<expr> {node.__class__.__name__} <expr>'
        left = self.visit(node.left, tabs + 1)
        right = self.visit(node.right, tabs + 1)
        return f'{ans}\n{left}\n{right}'

    @visitor.when(AtomicNode)
    def visit(self, node, tabs=0):
        return '\t' * tabs + f'\\__ {node.__class__.__name__}: {node.lex}'
    
    @visitor.when(CallNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\__CallNode: {node.lex}(<expr>, ..., <expr>)'
        args = '\n'.join(self.visit(arg, tabs + 1) for arg in node.args)
        return f'{ans}\n{args}'
    

class VariableInfo:
    def __init__(self, name):
        self.name = name

class FunctionInfo:
    def __init__(self, name, params):
        self.name = name
        self.params = params

class Scope:
    def __init__(self, parent=None):
        self.local_vars = []
        self.local_funcs = []
        self.parent = parent
        self.children = []
        self.var_index_at_parent = 0 if parent is None else len(parent.local_vars)
        self.func_index_at_parent = 0 if parent is None else len(parent.local_funcs)
        
    def create_child_scope(self):
        child_scope = Scope(self)
        self.children.append(child_scope)
        return child_scope

    def define_variable(self, vname):
        if self.is_local_var(vname):
            return False
        self.local_vars.append(VariableInfo(vname))
        return True
    
    def define_function(self, fname, params):
        if self.is_local_func(fname,len(params)):
            return False
        self.local_vars.append(FunctionInfo(fname,params))
        return True

    def is_var_defined(self, vname):  
        return self.is_local_var(vname) or (self.parent.is_var_defined(vname) if self.parent is not None else False)    
    
    def is_func_defined(self, fname, n):    
        return self.is_local_func(fname,n) or (self.parent.is_func_defined(fname,n) if self.parent is not None else False)

    def is_local_var(self, vname):
        return self.get_local_variable_info(vname) is not None
    
    def is_local_func(self, fname, n):
        return self.get_local_function_info(fname, n) is not None

    def get_local_variable_info(self, vname):
        for var_info in self.local_vars:
            if vname == var_info.name:
                return var_info
        return None
    
    def get_local_function_info(self, fname, n):
        for func_info in self.local_funcs:
            if fname == func_info.name and n == len(func_info.params):
                return func_info
        return None       

class SemanticCheckerVisitor(object):
    def __init__(self):
        self.errors = []
    
    @visitor.on('node')
    def visit(self, node, scope):
        pass
    
    @visitor.when(ProgramNode)
    def visit(self, node, scope=None):
        if scope is None:
            scope = Scope()
        for statement_node in node.statements:
            self.visit(statement_node, scope)
        return self.errors
    
    @visitor.when(VarDeclarationNode)
    def visit(self, node, scope):
        self.visit(node.expr, scope) 
        if not scope.define_variable(node.id):
            self.errors.append(f'Variable {node.id} is already defined in current scope.')       
    
    @visitor.when(FuncDeclarationNode)
    def visit(self, node, scope):
        inner_scope = scope.create_child_scope()
        for param in node.params:
            if not inner_scope.define_variable(param):
                self.errors.append(f'Function {node.id} is invalid, its arguments have to be different from each other.')
        self.visit(node.body,inner_scope)
        if not scope.define_function(node.id, node.params):
            self.errors.append(f'Function {node.id} is already defined with {len(node.params)} arguments.')
    
    @visitor.when(PrintNode)
    def visit(self, node, scope):
        self.visit(node.expr, scope)
    
    @visitor.when(ConstantNumNode)
    def visit(self, node, scope):
        pass
    
    @visitor.when(VariableNode)
    def visit(self, node, scope):
        if not scope.is_var_defined(node.lex):
            self.errors.append(f'Variable {node.lex} is not defined.')
    
    @visitor.when(CallNode)
    def visit(self, node, scope):
        for argument_node in node.args:
            self.visit(argument_node,scope)
        if not scope.is_func_defined(node.lex,len(node.args)):
            self.errors.append(f'Function {node.lex} is not defined with {len(node.args)} arguments.')
    
    @visitor.when(BinaryNode)
    def visit(self, node, scope):
        self.visit(node.left,scope)
        self.visit(node.right,scope)
