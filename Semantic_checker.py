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
class ProgramNode:
    def __init__(self, program, expr):
        self.program = program
        self.expr = expr

    def evaluate(self):
        # Implementación de la evaluación del programa
        pass

class FunctionStatNode:
    def __init__(self, function_, id_, params, id_extend, body):
        self.function_ = function_
        self.id_ = id_
        self.params = params
        self.id_extend = id_extend
        self.body = body

    def evaluate(self):
        # Implementación de la evaluación de la declaración de función
        pass

class TypeStatNode:
    def __init__(self, type_, id_, params_in_par, inherits_expr, decls_methods_semi):
        self.type_ = type_
        self.id_ = id_
        self.params_in_par = params_in_par
        self.inherits_expr = inherits_expr
        self.decls_methods_semi = decls_methods_semi

    def evaluate(self):
        # Implementación de la evaluación de la declaración de tipo
        pass

class ProtocolStatNode:
    def __init__(self, protocol, id_, extends_expr, method_protocol_list):
        self.protocol = protocol
        self.id_ = id_
        self.extends_expr = extends_expr
        self.method_protocol_list = method_protocol_list

    def evaluate(self):
        # Implementación de la evaluación de la declaración de protocolo
        pass

class MethodProtocolNode:
    def __init__(self, id_, params, id_extend):
        self.id_ = id_
        self.params = params
        self.id_extend = id_extend

    def evaluate(self):
        # Implementación de la evaluación del método de protocolo
        pass

class MethodNode:
    def __init__(self, id_, params, id_extend, body):
        self.id_ = id_
        self.params = params
        self.id_extend = id_extend
        self.body = body

    def evaluate(self):
        # Implementación de la evaluación del método
        pass

class ExtendsExprNode:
    def __init__(self, extends, id_):
        self.extends = extends
        self.id_ = id_

    def evaluate(self):
        # Implementación de la evaluación de la expresión de extensión
        pass

class InheritsExprNode:
    def __init__(self, inherits, id_, args_in_par):
        self.inherits = inherits
        self.id_ = id_
        self.args_in_par = args_in_par

    def evaluate(self):
        # Implementación de la evaluación de la expresión de herencia
        pass

class BodyNode:
    def __init__(self, expr):
        self.expr = expr

    def evaluate(self):
        # Implementación de la evaluación del cuerpo
        pass

class ParamsNode:
    def __init__(self, params_aux):
        self.params_aux = params_aux

    def evaluate(self):
        # Implementación de la evaluación de los parámetros
        pass

class ParamsAuxNode:
    def __init__(self, id_, type_):
        self.id_ = id_
        self.type_ = type_

    def evaluate(self):
        # Implementación de la evaluación de los parámetros auxiliares
        pass

class ParamsInParNode:
    def __init__(self, params):
        self.params = params

    def evaluate(self):
        # Implementación de la evaluación de los parámetros entre paréntesis
        pass

class ExprNode:
    def __init__(self, expr_type, expr):
        self.expr_type = expr_type
        self.expr = expr

    def evaluate(self):
        # Implementación de la evaluación de la expresión
        pass

class InstExprNode:
    def __init__(self, new_, id_, args):
        self.new_ = new_
        self.id_ = id_
        self.args = args

    def evaluate(self):
        # Implementación de la evaluación de la expresión de instanciación
        pass

class ArrayExprNode:
    def __init__(self, new_, id_, expr):
        self.new_ = new_
        self.id_ = id_
        self.expr = expr

    def evaluate(self):
        # Implementación de la evaluación de la expresión de arreglo
        pass

class PrintExprNode:
    def __init__(self, print_, expr):
        self.print_ = print_
        self.expr = expr

    def evaluate(self):
        # Implementación de la evaluación de la expresión de impresión
        pass

class LetExprNode:
    def __init__(self, decls,expr_body):
        self.decls = decls
        self.expr_body = expr_body

    def evaluate(self):
        # Implementación de la evaluación de la expresión de declaración
        pass

class DestrExprNode:
    def __init__(self, loc, expr):
        self.loc = loc
        self.expr = expr

    def evaluate(self):
        # Implementación de la evaluación de la expresión de destrucción
        pass

class WhileExprNode:
    def __init__(self, expr, expr_body):
        self.expr = expr
        self.expr_body = expr_body

    def evaluate(self):
        # Implementación de la evaluación de la expresión de ciclo while
        pass

class ForExprNode:
    def __init__(self,id_, expr, expr_body):
        self.id_ = id_
        self.expr = expr
        self.expr_body = expr_body

    def evaluate(self):
        # Implementación de la evaluación de la expresión de ciclo for
        pass

class IfExprNode:
    def __init__(self,expr, expr_body, elif_expr):
        self.expr = expr
        self.expr_body = expr_body
        self.elif_expr = elif_expr

    def evaluate(self):
        # Implementación de la evaluación de la expresión condicional if
        pass

class ElifExprNode:
    def __init__(self, expr, expr_body, elif_expr):
        self.expr = expr
        self.expr_body = expr_body
        self.elif_expr = elif_expr

    def evaluate(self):
        # Implementación de la evaluación de la expresión condicional elif
        pass

class ElseExprNode:
    def __init__(self, expr_body):
        self.expr_body = expr_body

    def evaluate(self):
        # Implementación de la evaluación de la expresión condicional else
        pass

class DeclNode:
    def __init__(self, id_, id_extend, expr):
        self.id_ = id_
        self.id_extend = id_extend
        self.expr = expr

    def evaluate(self):
        # Implementación de la evaluación de la declaración
        pass

class DeclsNode:
    def __init__(self, decls, decl):
        self.decls = decls
        self.decl = decl

    def evaluate(self):
        # Implementación de la evaluación del conjunto de declaraciones
        pass

class ExprBodyNode:
    def __init__(self, expr):
        self.expr = expr

    def evaluate(self):
        # Implementación de la evaluación del cuerpo de la expresión
        pass

class ExprListSemiNode:
    def __init__(self, expr_list_semi, expr):
        self.expr_list_semi = expr_list_semi
        self.expr = expr

    def evaluate(self):
        # Implementación de la evaluación de la lista de expresiones separadas por punto y coma
        pass

class IdExtendNode:
    def __init__(self, id_):
        self.id_ = id_

    def evaluate(self):
        # Implementación de la evaluación de la extensión de identificador
        pass

class ExprElemNode:
    def __init__(self, expr_elem, as_expr):
        self.expr_elem = expr_elem
        self.as_expr = as_expr

    def evaluate(self):
        # Implementación de la evaluación del elemento de expresión
        pass

class AsExprNode:
    def __init__(self, as_expr, logic_concat_expr):
        self.as_expr = as_expr
        self.logic_concat_expr = logic_concat_expr

    def evaluate(self):
        # Implementación de la evaluación de la expresión de conversión de tipo
        pass

class LogicConcatExprNode:
    def __init__(self, logic_concat_expr, comp_expr):
        self.logic_concat_expr = logic_concat_expr
        self.comp_expr = comp_expr

    def evaluate(self):
        # Implementación de la evaluación de la expresión de concatenación lógica
        pass

class CompExprNode:
    def __init__(self, comp_expr, aritm_expr):
        self.comp_expr = comp_expr
        self.aritm_expr = aritm_expr

    def evaluate(self):
        # Implementación de la evaluación de la expresión de comparación
        pass

class AritmExprNode:
    def __init__(self, aritm_expr, term):
        self.aritm_expr = aritm_expr
        self.term = term

    def evaluate(self):
        # Implementación de la evaluación de la expresión aritmética
        pass

class TermNode:
    def __init__(self, term, pow_expr):
        self.term = term
        self.pow_expr = pow_expr

    def evaluate(self):
        # Implementación de la evaluación del término aritmético
        pass

class PowExprNode:
    def __init__(self, pow_expr, negative):
        self.pow_expr = pow_expr
        self.negative = negative

    def evaluate(self):
        # Implementación de la evaluación de la expresión de potencia
        pass

class NegativeNode:
    def __init__(self, factor):
        self.factor = factor

    def evaluate(self):
        # Implementación de la evaluación de la expresión negativa
        pass

class FactorNode:
    def __init__(self, expr, params_aux,expr2):
        self.expr = expr
        self.params_aux = params_aux
        self.expr2 = expr2

    def evaluate(self):
        # Implementación de la evaluación del factor de expresión
        pass

class LocNode:
    def __init__(self, loc, id_, args_in_par):
        self.loc = loc
        self.id_ = id_
        self.args_in_par = args_in_par

    def evaluate(self):
        # Implementación de la evaluación de la ubicación
        pass

class ArgsNode:
    def __init__(self, args_aux):
        self.args_aux = args_aux

    def evaluate(self):
        # Implementación de la evaluación de los argumentos
        pass

class ArgsAuxNode:
    def __init__(self, args_aux, expr):
        self.args_aux = args_aux
        self.expr = expr

    def evaluate(self):
        # Implementación de la evaluación de los argumentos auxiliares
        pass

class ArgsInParNode:
    def __init__(self, args):
        self.args = args

    def evaluate(self):
        # Implementación de la evaluación de los argumentos entre paréntesis
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
    
    @visitor.when(PrintExprNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\__PrintExprNode <expr>'
        expr = self.visit(node.expr, tabs + 1)
        return f'{ans}\n{expr}'
    
    # @visitor.when(VarDeclarationNode)
    # def visit(self, node, tabs=0):
    #     ans = '\t' * tabs + f'\\__VarDeclarationNode: let {node.id} = <expr>'
    #     expr = self.visit(node.expr, tabs + 1)
    #     return f'{ans}\n{expr}'
    
    # @visitor.when(FuncDeclarationNode)
    # def visit(self, node, tabs=0):
    #     params = ', '.join(node.params)
    #     ans = '\t' * tabs + f'\\__FuncDeclarationNode: def {node.id}({params}) -> <expr>'
    #     body = self.visit(node.body, tabs + 1)
    #     return f'{ans}\n{body}'

    @visitor.when(BinaryNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\__<expr> {node.__class__.__name__} <expr>'
        left = self.visit(node.left, tabs + 1)
        right = self.visit(node.right, tabs + 1)
        return f'{ans}\n{left}\n{right}'

    @visitor.when(AtomicNode)
    def visit(self, node, tabs=0):
        return '\t' * tabs + f'\\__ {node.__class__.__name__}: {node.lex}'
    
    # @visitor.when(CallNode)
    # def visit(self, node, tabs=0):
    #     ans = '\t' * tabs + f'\\__CallNode: {node.lex}(<expr>, ..., <expr>)'
    #     args = '\n'.join(self.visit(arg, tabs + 1) for arg in node.args)
    #     return f'{ans}\n{args}'
    

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
    
    # @visitor.when(VarDeclarationNode)
    # def visit(self, node, scope):
    #     self.visit(node.expr, scope) 
    #     if not scope.define_variable(node.id):
    #         self.errors.append(f'Variable {node.id} is already defined in current scope.')       
    
    # @visitor.when(FuncDeclarationNode)
    # def visit(self, node, scope):
    #     inner_scope = scope.create_child_scope()
    #     for param in node.params:
    #         if not inner_scope.define_variable(param):
    #             self.errors.append(f'Function {node.id} is invalid, its arguments have to be different from each other.')
    #     self.visit(node.body,inner_scope)
    #     if not scope.define_function(node.id, node.params):
    #         self.errors.append(f'Function {node.id} is already defined with {len(node.params)} arguments.')
    
    @visitor.when(PrintExprNode)
    def visit(self, node, scope):
        self.visit(node.expr, scope)
    
    # @visitor.when(ConstantNumNode)
    # def visit(self, node, scope):
    #     pass
    
    # @visitor.when(VariableNode)
    # def visit(self, node, scope):
    #     if not scope.is_var_defined(node.lex):
    #         self.errors.append(f'Variable {node.lex} is not defined.')
    
    # @visitor.when(CallNode)
    # def visit(self, node, scope):
    #     for argument_node in node.args:
    #         self.visit(argument_node,scope)
    #     if not scope.is_func_defined(node.lex,len(node.args)):
    #         self.errors.append(f'Function {node.lex} is not defined with {len(node.args)} arguments.')
    
    @visitor.when(BinaryNode)
    def visit(self, node, scope):
        self.visit(node.left,scope)
        self.visit(node.right,scope)
