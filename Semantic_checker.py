from Automata import *
from Grammar import *
from Parser import *
from ParserLR1 import *
from Regex import *

#Metodos auxiliares

#del evaluation
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
    def __init__(self, statements):
        self.statements = statements
        
class StatementNode(Node):
    pass
        
class ExpressionNode(Node):
    pass

class VarDeclarationNode(StatementNode):
    def __init__(self, idx, expr):
        self.id = idx
        self.expr = expr

class FuncDeclarationNode(StatementNode):
    def __init__(self, idx, params, body):
        self.id = idx
        self.params = params
        self.body = body

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


########ME imagino que haya que poner mas clases de nodes



#endregion

#region ejemplo de gramatica
G = Grammar()

program = G.NonTerminal('<program>', startSymbol=True)
stat_list, stat = G.NonTerminals('<stat_list> <stat>')
let_var, def_func, print_stat, arg_list = G.NonTerminals('<let-var> <def-func> <print-stat> <arg-list>')
expr, term, factor, atom = G.NonTerminals('<expr> <term> <factor> <atom>')
func_call, expr_list = G.NonTerminals('<func-call> <expr-list>')

let, defx, printx = G.Terminals('let def print')
semi, comma, opar, cpar, arrow = G.Terminals('; , ( ) ->')
equal, plus, minus, star, div = G.Terminals('= + - * /')
idx, num = G.Terminals('id int')

program %= stat_list, lambda h,s: ProgramNode(s[1])

stat_list %= stat + semi, lambda h,s: [s[1]] # Your code here!!! (add rule)
stat_list %= stat + semi + stat_list, lambda h,s: [s[1]] + s[3] # Your code here!!! (add rule)

stat %= let_var, lambda h,s: s[1] # Your code here!!! (add rule)
stat %= def_func, lambda h,s: s[1] # Your code here!!! (add rule)
stat %= print_stat, lambda h,s: s[1] # Your code here!!! (add rule)

let_var %= let + idx + equal + expr, lambda h,s: VarDeclarationNode(s[2], s[4]) # Your code here!!! (add rule)

def_func %= defx + idx + opar + arg_list + cpar + arrow + expr, lambda h,s: FuncDeclarationNode(s[2], s[4], s[7]) # Your code here!!! (add rule)

print_stat %= printx + expr, lambda h,s: PrintNode(s[2]) # Your code here!!! (add rule)

arg_list %= idx, lambda h,s: [s[1]] # Your code here!!! (add rule)
arg_list %= idx + comma + arg_list, lambda h,s: [s[1]] + s[3] # Your code here!!! (add rule)

expr %= expr + plus + term, lambda h,s: PlusNode(s[1],s[3]) # Your code here!!! (add rule)
expr %= expr + minus + term, lambda h,s: MinusNode(s[1],s[3]) # Your code here!!! (add rule)
expr %= term, lambda h,s: s[1] # Your code here!!! (add rule)

term %= term + star + factor, lambda h,s: StarNode(s[1],s[3]) # Your code here!!! (add rule)
term %= term + div + factor, lambda h,s: DivNode(s[1],s[3]) # Your code here!!! (add rule)
term %= factor, lambda h,s: s[1] # Your code here!!! (add rule)

factor %= atom, lambda h,s: s[1] # Your code here!!! (add rule)
factor %= opar + expr + cpar, lambda h,s: s[2] # Your code here!!! (add rule)

atom %= num, lambda h,s: ConstantNumNode(s[1]) # Your code here!!! (add rule)
atom %= idx, lambda h,s: VariableNode(s[1]) # Your code here!!! (add rule)
atom %= func_call, lambda h,s: s[1] # Your code here!!! (add rule)

func_call %= idx + opar + expr_list + cpar, lambda h,s: CallNode(s[1], s[3]) # Your code here!!! (add rule)

expr_list %= expr, lambda h,s: [s[1]] # Your code here!!! (add rule)
expr_list %= expr + comma + expr_list, lambda h,s: [s[1]] + s[3] # Your code here!!! (add rule)

tokens = [
    Token('print', printx),
    Token('1', num),
    Token('-', minus),
    Token('1', num),
    Token('-', minus),
    Token('1', num),
    Token(';', semi),
    Token('let', let),
    Token('x', idx),
    Token('=', equal),
    Token('58', num),
    Token(';', semi),
    Token('def', defx),
    Token('f', idx),
    Token('(', opar),
    Token('a', idx),
    Token(',', comma),
    Token('b', idx),
    Token(')', cpar),
    Token('->', arrow),
    Token('5', num),
    Token('+', plus),
    Token('6', num),
    Token(';', semi),
    Token('print', printx),
    Token('F', idx),
    Token('(', opar),
    Token('5', num),
    Token('+', plus),
    Token('x', idx),
    Token(',', comma),
    Token('7', num),
    Token('+', plus),
    Token('y', idx),
    Token(')', cpar),
    Token(';', semi),
    Token('$', G.EOF),
]
#endregion




#########################################################INICIO########################################################
#inicializando con las cosas del parser

parser = LR1Parser(G)
parse,operations = parser([t.token_type for t in tokens], get_shift_reduce=True)


#obtener la raiz del ast

ast = evaluate_reverse_parse(parse, operations, tokens)

#metodo visitor para recorrer el ast y poder imprimirlo

import Visitor as visitor

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
    


#imprimiendo el ast
formatter = FormatVisitor()
print(formatter.visit(ast))

#clases pal checkeo

class VariableInfo:
    def __init__(self, name):
        self.name = name

class FunctionInfo:
    def __init__(self, name, params):
        self.name = name
        self.params = params

# para ocultar las variables

import itertools as itl

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
        # Your code here!!!
        if self.is_local_var(vname):
            return False
        self.local_vars.append(VariableInfo(vname))
        return True
    
    def define_function(self, fname, params):
        # Your code here!!!
        if self.is_local_func(fname,len(params)):
            return False
        self.local_vars.append(FunctionInfo(fname,params))
        return True

    def is_var_defined(self, vname):   # ARREGLAR: BUSCAR EN PARENT SOLO HASTA VAR_INDEX_AT_PARENT
        # Your code here!!!
        return self.is_local_var(vname) or (self.parent.is_var_defined(vname) if self.parent is not None else False)    
    
    def is_func_defined(self, fname, n):     # ARREGLAR: BUSCAR EN PARENT SOLO HASTA FUNC_INDEX_AT_PARENT
        # Your code here!!!
        return self.is_local_func(fname,n) or (self.parent.is_func_defined(fname,n) if self.parent is not None else False)

    def is_local_var(self, vname):
        return self.get_local_variable_info(vname) is not None
    
    def is_local_func(self, fname, n):
        return self.get_local_function_info(fname, n) is not None

    def get_local_variable_info(self, vname):
        # Your code here!!!
        for var_info in self.local_vars:
            if vname == var_info.name:
                return var_info
        return None
    
    def get_local_function_info(self, fname, n):
        # Your code here!!!
        for func_info in self.local_funcs:
            if fname == func_info.name and n == len(func_info.params):
                return func_info
        return None       
    
    
scope = Scope()

#Checkeo total

class SemanticCheckerVisitor(object):
    def __init__(self):
        self.errors = []
    
    @visitor.on('node')
    def visit(self, node, scope):
        pass
    
    @visitor.when(ProgramNode)
    def visit(self, node, scope=None):
        # Your code here!!!
        if scope is None:
            scope = Scope()
        for statement_node in node.statements:
            self.visit(statement_node, scope)
        return self.errors
    
    @visitor.when(VarDeclarationNode)
    def visit(self, node, scope):
        # Your code here!!!                                      
        self.visit(node.expr, scope) 
        if not scope.define_variable(node.id):
            self.errors.append(f'Variable {node.id} is already defined in current scope.')       
    
    @visitor.when(FuncDeclarationNode)
    def visit(self, node, scope):
        # Your code here!!!        
        inner_scope = scope.create_child_scope()
        for param in node.params:
            if not inner_scope.define_variable(param):
                self.errors.append(f'Function {node.id} is invalid, its arguments have to be different from each other.')
        self.visit(node.body,inner_scope)
        if not scope.define_function(node.id, node.params):
            self.errors.append(f'Function {node.id} is already defined with {len(node.params)} arguments.')
    
    @visitor.when(PrintNode)
    def visit(self, node, scope):
        # Your code here!!!
        self.visit(node.expr, scope)
    
    @visitor.when(ConstantNumNode)
    def visit(self, node, scope):
        # Your code here!!!
        pass
    
    @visitor.when(VariableNode)
    def visit(self, node, scope):
        # Your code here!!!
        if not scope.is_var_defined(node.lex):
            self.errors.append(f'Variable {node.lex} is not defined.')
    
    @visitor.when(CallNode)
    def visit(self, node, scope):
        # Your code here!!!
        for argument_node in node.args:
            self.visit(argument_node,scope)
        if not scope.is_func_defined(node.lex,len(node.args)):
            self.errors.append(f'Function {node.lex} is not defined with {len(node.args)} arguments.')
    
    @visitor.when(BinaryNode)
    def visit(self, node, scope):
        # Your code here!!!
        self.visit(node.left,scope)
        self.visit(node.right,scope)

#printeando los errores

semantic_checker = SemanticCheckerVisitor()
errors = semantic_checker.visit(ast)
for i, error in enumerate(errors,1):
    print(f'{i}.', error)