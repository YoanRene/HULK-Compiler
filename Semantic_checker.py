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
    def __init__(self,id_, params, id_extend, body):
        self.id_ = id_
        self.params = params
        self.id_extend = id_extend
        self.body = body

    def evaluate(self):
        # Implementación de la evaluación de la declaración de función
        pass

class TypeStatNode:
    def __init__(self, id_, params_in_par, inherits_expr, decls_methods_semi):
        self.id_ = id_
        self.params_in_par = params_in_par
        self.inherits_expr = inherits_expr
        self.decls_methods_semi = decls_methods_semi

    def evaluate(self):
        # Implementación de la evaluación de la declaración de tipo
        pass

class ProtocolStatNode:
    def __init__(self, id_, extends_expr, method_protocol_list):
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
    def __init__(self, id_):
        self.id_ = id_

    def evaluate(self):
        # Implementación de la evaluación de la expresión de extensión
        pass

class InheritsExprNode:
    def __init__(self, id_, args_in_par):
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
    def __init__(self, id_, id_extend):
        self.id_ = id_
        self.id_extend = id_extend

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
    def __init__(self, id_, args):
        self.id_ = id_
        self.args = args

    def evaluate(self):
        # Implementación de la evaluación de la expresión de instanciación
        pass

class ArrayExprNode:
    def __init__(self, id_, expr):
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
        expr = self.visit(node.expr, tabs + 1)
        return f'{ans}\n{expr}'
    
    @visitor.when(PrintExprNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\__PrintExprNode <expr>'
        expr = self.visit(node.expr, tabs + 1)
        return f'{ans}\n{expr}'
    
    @visitor.when(DeclsNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\__DeclsNode'
        decls = self.visit(node.decls, tabs + 1)
        decl=self.visit(node.decl, tabs + 1)
        return f'{ans}\n{decls}\n{decl}'
    
    @visitor.when(DeclNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\__DeclNode <id> : <type>'
        id= self.visit(node.id_, tabs + 1)
        id_extend = self.visit(node.id_extend, tabs + 1)
        expr = self.visit(node.expr, tabs + 1)
        
        return f'{ans}\n{id}\n{id_extend}\n{expr}'
    
    @visitor.when(FunctionStatNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\__FunctionStatNode <id> (<params>) : <type> <block>'
        id = self.visit(node.id_, tabs + 1)
        params = self.visit(node.params, tabs + 1)
        id_extend = self.visit(node.id_extend, tabs + 1)
        body = self.visit(node.body, tabs + 1)

    
    @visitor.when(TypeStatNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\__TypeStatNode <id> : <type>'
        id = self.visit(node.id_, tabs + 1)
        params_in_par = self.visit(node.params_in_par, tabs + 1)
        inherits_expr = self.visit(node.inherits_expr, tabs + 1)
        decls_method_semi = self.visit(node.decls_method_semi, tabs + 1)

        return f'{ans}\n{id}\n{params_in_par}\n{inherits_expr}\n{decls_method_semi}'
    
    @visitor.when(ProtocolStatNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\__ProtocolStatNode <id> : <type>'
        id = self.visit(node.id_, tabs + 1)
        extends_expr = self.visit(node.extends_expr, tabs + 1)
        method_protocol_list= self.visit(node.method_protocol_list, tabs + 1)

        return f'{ans}\n{id}\n{extends_expr}\n{method_protocol_list}'
    
    @visitor.when(MethodProtocolNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\__MethodProtocolNode <id> (<params>) : <type>'
        id = self.visit(node.id_, tabs + 1)
        params = self.visit(node.params, tabs + 1)
        id_extend = self.visit(node.id_extend, tabs + 1)
        return f'{ans}\n{id}\n{params}\n{id_extend}'
    
    @visitor.when(ExtendsExprNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\__ExtendsExprNode <id>'
        id = self.visit(node.id_, tabs + 1)
        return f'{ans}\n{id}'


    @visitor.when(InheritsExprNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\__InheritsExprNode <id>'
        id = self.visit(node.id_, tabs + 1)
        args_in_par = self.visit(node.args_in_par, tabs + 1)
        return f'{ans}\n{id}\n{args_in_par}'
    
    @visitor.when(MethodNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\__MethodNode <id> (<params>) : <type> <block>'
        id = self.visit(node.id_, tabs + 1)
        params = self.visit(node.params, tabs + 1)
        id_extend = self.visit(node.id_extend, tabs + 1)
        body = self.visit(node.body, tabs + 1)
        return f'{ans}\n{id}\n{params}\n{id_extend}\n{body}'
    
    @visitor.when(BodyNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\__BodyNode <expr>; ... <expr>;'
        expr = '\n'.join(self.visit(child, tabs + 1) for child in node.expr)
        return f'{ans}\n{expr}'
    
    @visitor.when(ParamsAuxNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\__ParamsAuxNode <id> : <type>'
        id = self.visit(node.id_, tabs + 1)
        id_extend = self.visit(node.id_extend, tabs + 1)
        return f'{ans}\n{id}\n{id_extend}'
    
    @visitor.when(ParamsNode) #######################
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\__ParamsNode <id> : <type>'
        params_aux = self.visit(node.params_aux, tabs + 1)
        return f'{ans}\n{params_aux}'
    
    @visitor.when(ParamsInParNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\__ParamsInParNode <id> : <type>'
        params= self.visit(node.params, tabs + 1)
        return f'{ans}\n{params}'
    
    @visitor.when(InstExprNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\__InstExprNode <id>'
        id = self.visit(node.id_, tabs + 1)
        args= self.visit(node.args, tabs + 1)
        return f'{ans}\n{id}\n{args}'
    
    @visitor.when(ArrayExprNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\__ArrayExprNode <expr>'
        id= self.visit(node.id_, tabs + 1)
        expr = self.visit(node.expr, tabs + 1)
        return f'{ans}\n{id}\n{expr}'
    
    @visitor.when(LetExprNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\__LetExprNode <id> : <type> = <expr> in <expr>' ##############
        decls= self.visit(node.decls, tabs + 1)
        expr_body = self.visit(node.expr_body, tabs + 1)

        return f'{ans}\n{decls}\n{expr_body}'
    
    @visitor.when(DestrExprNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\__DestrExprNode <expr> = <expr>'
        loc = self.visit(node.loc, tabs + 1)
        expr = self.visit(node.expr, tabs + 1)
        return f'{ans}\n{loc}\n{expr}'
    
    @visitor.when(WhileExprNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\__WhileExprNode <expr> = <expr_body>'
        expr= self.visit(node.expr, tabs + 1)
        expr_body = self.visit(node.expr_body, tabs + 1)

        return f'{ans}\n{expr}\n{expr_body}'
    
    @visitor.when(ForExprNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\__ForExprNode <id> = <expr> <expr_body>'
        id = self.visit(node.id_, tabs + 1)
        expr = self.visit(node.expr, tabs + 1)
        expr_body = self.visit(node.expr_body, tabs + 1)
        return f'{ans}\n{id}\n{expr}\n{expr_body}'
    
    @visitor.when(IfExprNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\__IfExprNode <expr> <expr_body> elif <expr>'
        expr = self.visit(node.expr, tabs + 1)
        expr_body = self.visit(node.expr_body, tabs + 1)
        elif_expr = self.visit(node.elif_expr, tabs + 1)
        return f'{ans}\n{expr}\n{expr_body}\n{elif_expr}'
    
    @visitor.when(ElifExprNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\__ElifExprNode <expr> <expr_body> <elif_expr>'
        expr = self.visit(node.expr, tabs + 1)
        expr_body = self.visit(node.expr_body, tabs + 1)
        elif_expr = self.visit(node.elif_expr, tabs + 1)
        return f'{ans}\n{expr}\n{expr_body}\n{elif_expr}'
    
    @visitor.when(ElseExprNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\__ElseExprNode <expr_body>'
        expr_body = self.visit(node.expr_body, tabs + 1)
        return f'{ans}\n{expr_body}'
    
    @visitor.when(DeclNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\__DeclNode <id> : <type> = <expr>'
        id = self.visit(node.id_, tabs + 1)
        id_extend = self.visit(node.id_extend, tabs + 1)
        expr = self.visit(node.expr, tabs + 1)
        return f'{ans}\n{id}\n{id_extend}\n{expr}'
    
    @visitor.when(ExprBodyNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\__ExprBodyNode <expr>'
        expr = self.visit(node.expr, tabs + 1)
        return f'{ans}\n{expr}'
    
    @visitor.when(ExprListSemiNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\__ExprListSemiNode <expr> <expr_list>'
        expr_list_semi = self.visit(node.expr_list_semi, tabs + 1)
        expr = self.visit(node.expr, tabs + 1)
        return f'{ans}\n{expr_list_semi}\n{expr}'
    
    @visitor.when(IdExtendNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\__IdExtendNode <id> <id_extend>'
        id = self.visit(node.id_, tabs + 1)
        return f'{ans}\n{id}'
    
    @visitor.when(ExprElemNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\__ExprElemNode <expr> <expr_elem>'
        expr_elem = self.visit(node.expr_elem, tabs + 1)
        as_expr = self.visit(node.as_expr, tabs + 1)
        return f'{ans}\n{expr_elem}\n{as_expr}'
    
    @visitor.when(AsExprNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\__AsExprNode <expr>'
        as_expr = self.visit(node.as_expr, tabs + 1)
        logic_concat_expr = self.visit(node.logic_concat_expr, tabs + 1)

        return f'{ans}\n{as_expr}\n{logic_concat_expr}'
    
    @visitor.when(LogicConcatExprNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\__LogicConcatExprNode <expr> <logic_concat_expr>'
        logic_concat_expr = self.visit(node.logic_concat_expr, tabs + 1)
        comp_expr = self.visit(node.comp_expr, tabs + 1)
        return f'{ans}\n{logic_concat_expr}\n{comp_expr}'
    
    @visitor.when(CompExprNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\__CompExprNode <expr> <comp_expr>'
        comp_expr = self.visit(node.comp_expr, tabs + 1)
        aritm_expr = self.visit(node.aritm_expr, tabs + 1)
        return f'{ans}\n{comp_expr}\n{aritm_expr}'
    
    @visitor.when(AritmExprNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\__AritmExprNode <expr> <aritm_expr>'
        aritm_expr = self.visit(node.aritm_expr, tabs + 1)
        term = self.visit(node.term, tabs + 1)
        return f'{ans}\n{aritm_expr}\n{term}'
    
    @visitor.when(TermNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\__TermNode <expr> <term>'
        term = self.visit(node.term, tabs + 1)
        pow_expr = self.visit(node.pow_expr, tabs + 1)
        return f'{ans}\n{term}\n{pow_expr}'
    
    @visitor.when(PowExprNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\__PowExprNode <expr> <pow_expr>'
        pow_expr = self.visit(node.pow_expr, tabs + 1)
        negative = self.visit(node.negative, tabs + 1)
        return f'{ans}\n{pow_expr}\n{negative}'
    
    @visitor.when(NegativeNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\__NegativeNode <expr>'
        factor = self.visit(node.factor, tabs + 1)
        return f'{ans}\n{factor}'
    
    @visitor.when(FactorNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\__FactorNode <expr>'
        expr = self.visit(node.expr, tabs + 1)
        params_aux = self.visit(node.params_aux, tabs + 1)
        expr2 = self.visit(node.expr2, tabs + 1)
        return f'{ans}\n{expr}\n{params_aux}\n{expr2}'
    
    @visitor.when(LocNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\__LocNode <expr>'
        loc = self.visit(node.loc, tabs + 1)
        id= self.visit(node.id_, tabs + 1)
        args_in_par = self.visit(node.args_in_par, tabs + 1)
        return f'{ans}\n{loc}\n{id}\n{args_in_par}'
    
    @visitor.when(ArgsAuxNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\__ArgsAuxNode <expr> <args_aux>'
        args_aux = self.visit(node.args_aux, tabs + 1)
        expr = self.visit(node.expr, tabs + 1)
        return f'{ans}\n{args_aux}\n{expr}'
    
    @visitor.when(ArgsNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\__ArgsNode <expr>'
        args_aux = self.visit(node.args_aux, tabs + 1)

        return f'{ans}\n{args_aux}'
    
    @visitor.when(ArgsInParNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\__ArgsInParNode <expr>'
        args = self.visit(node.args, tabs + 1)
        return f'{ans}\n{args}'
    

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



    ##################Parte de nosotros

    @visitor.when(ProgramNode)
    def visit(self, node, scope=None):
        if scope is None:
            scope = Scope()
        self.visit(node.expr, scope)
        self.visit(node.program, scope)
        return self.errors

    @visitor.when(FunctionStatNode)
    def visit(self, node, scope):
        if not scope.define_function(node.id_, node.params):
            self.errors.append(f'Function {node.id} is already defined in current scope.')
        inner_scope = scope.create_child_scope()
        for param in node.params:
            if not inner_scope.define_variable(param):
                self.errors.append(f'Function {node.id_} is invalid, its arguments have to be different from each other.')
        self.visit(node.body, inner_scope)

    @visitor.when(TypeStatNode)
    def visit(self, node, scope):
        if not scope.define_variable(node.id_):
            self.errors.append(f'Variable {node.id_} is already defined in current scope.')
        
        if not scope.is_var_defined(node.inherit):
            self.errors.append(f'Variable {node.inherit} is not defined in current scope.')###############
        
        inner_scope = scope.create_child_scope()
        for param in node.params_in_par:
            if not inner_scope.define_variable(param):
                self.errors.append(f'Function {node.id_} is invalid, its arguments have to be different from each other.')

        
        self.visit(node.decls_methods_semi, inner_scope)

    @visitor.when(ProtocolStatNode)
    def visit(self, node, scope):
        if not scope.define_variable(node.id_):
            self.errors.append(f'Variable {node.id_} is already defined in current scope.')
        if not scope.is_var_defined(node.id_extends):
            self.errors.append(f'Variable {node.id_extends} is not defined in current scope.')
        inner_scope = scope.create_child_scope()

        self.visit(node.method_protocol_list, inner_scope)

    @visitor.when(MethodProtocolNode)
    def visit(self, node, scope):
        if not scope.define_function(node.id_, node.params):
            self.errors.append(f'Function {node.id_} is already defined in current scope.')
        if not scope.is_func_defined(node.id_extends, len(node.params)):
            self.errors.append(f'Function {node.id_extends} is not defined in current scope.')

        inner_scope = scope.create_child_scope()
        for param in node.params:
            if not inner_scope.define_variable(param):
                self.errors.append(f'Function {node.id_} is invalid, its arguments have to be different from each other.')
    
    @visitor.when(MethodNode)
    def visit(self, node, scope):
        if not scope.define_function(node.id_, node.params):
            self.errors.append(f'Function {node.id_} is already defined in current scope.')
        if not scope.is_func_defined(node.id_extends, len(node.params)):
            self.errors.append(f'Function {node.id_extends} is not defined in current scope.')
        inner_scope = scope.create_child_scope()
        for param in node.params:
            if not inner_scope.define_variable(param):
                self.errors.append(f'Function {node.id_} is invalid, its arguments have to be different from each other.')
        self.visit(node.body, inner_scope)

    @visitor.when(ExtendsExprNode)
    def visit(self, node, scope):
        pass

    @visitor.when(InheritsExprNode)
    def visit(self, node, scope):
        pass##################################################

    @visitor.when(BodyNode)
    def visit(self, node, scope):
        for exp in node.exprs:
            self.visit(exp, scope)

    @visitor.when(ParamsNode)
    def visit(self, node, scope):
        self.visit(node.params_aux, scope)

    @visitor.when(ParamsAuxNode)
    def visit(self, node, scope):
        if not scope.define_variable(node.id_):
            self.errors.append(f'Variable {node.id_} is already defined in current scope.')

        if not scope.is_var_defined(node.id_extends):
            self.errors.append(f'Variable {node.id_extends} is not defined in current scope.')
        
    @visitor.when(ParamsInParNode)
    def visit(self, node, scope):
        self.visit(node.params, scope)

    @visitor.when(InstExprNode)
    def visit(self, node, scope):
        if not scope.is_var_defined(node.id_):
            self.errors.append(f'Variable {node.id_} is not defined in current scope.')

        ########cantidad de parametros
        if not scope.is_func_defined(node.id_, len(node.params)):
            self.errors.append(f'Function {node.id_} is not defined in current scope.')########cambiar nombre de error
        
    
    @visitor.when(ArrayExprNode)
    def visit(self, node, scope):
        if not scope.is_var_defined(node.id_):
            self.errors.append(f'Variable {node.id_} is not defined in current scope.')
        self.visit(node.expr, scope)

    @visitor.when(PrintExprNode)
    def visit(self, node, scope):
        self.visit(node.expr, scope)

    @visitor.when(LetExprNode)
    def visit(self, node, scope):
        inner_scope = scope.create_child_scope()
        for decl in node.decls:##########################3
            self.visit(decl, inner_scope)
        self.visit(node.expr_body, inner_scope)

    @visitor.when(DestrExprNode)
    def visit(self, node, scope):
        self.visit(node.expr, scope)
        self.visit(node.loc, scope)

    @visitor.when(WhileExprNode)
    def visit(self, node, scope):
        #generame un if de si node.expr es una instancia de LogicConcatExprNode o un CompExprNode
        if node.expr.__class__.__name__ == 'LogicConcatExprNode' or node.expr.__class__.__name__ == 'CompExprNode':
            self.visit(node.expr, scope)
        else:
            self.errors.append(f'While condition must be a boolean expression.')
        inner_scope = scope.create_child_scope()
        self.visit(node.expr_body, inner_scope)

    @visitor.when(ForExprNode)
    def visit(self, node, scope):
        inner_scope = scope.create_child_scope()
        self.visit(node.expr_body, inner_scope)
    
    @visitor.when(IfExprNode)
    def visit(self, node, scope):
        #generame un if de si node.expr es una instancia de LogicConcatExprNode o un CompExprNode
        if node.expr.__class__.__name__ == 'LogicConcatExprNode' or node.expr.__class__.__name__ == 'CompExprNode':
            self.visit(node.expr, scope)
        else:
            self.errors.append(f'If condition must be a boolean expression.')
        inner_scope = scope.create_child_scope()
        self.visit(node.expr_body, inner_scope)
        self.visit(node.elif_expr, inner_scope)

    @visitor.when(ElifExprNode)#######
    def visit(self, node, scope):
        if node.expr is not None:
            #generame un if de si node.expr es una instancia de LogicConcatExprNode o un CompExprNode
            if node.expr.__class__.__name__ == 'LogicConcatExprNode' or node.expr.__class__.__name__ == 'CompExprNode':
                self.visit(node.expr, scope)
            else:
                self.errors.append(f'Elif condition must be a boolean expression.')
            inner_scope = scope.create_child_scope()
            self.visit(node.expr_body, inner_scope)
            self.visit(node.elif_expr, inner_scope)
    
    @visitor.when(ElseExprNode)
    def visit(self, node, scope):
        inner_scope = scope.create_child_scope()
        self.visit(node.expr_body, inner_scope)

    @visitor.when(DeclNode)
    def visit(self, node, scope):
        if not scope.define_variable(node.id_):
            self.errors.append(f'Variable {node.id_} is already defined in current scope.')
        if scope.is_var_defined(node.id_extend.id_):
            self.errors.append(f'Variable {node.id_extend.id_} is not defined in current scope.')
        self.visit(node.expr, scope)

    @visitor.when(DeclsNode)
    def visit(self, node, scope):
        self.visit(node.decls, scope)
        self.visit(node.decl, scope)
    
    @visitor.when(ExprBodyNode)
    def visit(self, node, scope):
        self.visit(node.expr, scope)
    
    @visitor.when(ExprListSemiNode)
    def visit(self, node, scope):
        self.visit(node.expr, scope)
        self.visit(node.expr_list_semi, scope)

    @visitor.when(IdExtendNode) ###################
    def visit(self, node, scope):
        if not scope.is_var_defined(node.id_):
            self.errors.append(f'Variable {node.id_} is not defined in current scope.')
    
    @visitor.when(ExprElemNode)
    def visit(self, node, scope):
        self.visit(node.expr_elem, scope)
        self.visit(node.as_expr, scope)

    @visitor.when(AsExprNode)
    def visit(self, node, scope):
        self.visit(node.as_expr, scope)
        self.visit(node.logic_concat_expr, scope)

    @visitor.when(LogicConcatExprNode)
    def visit(self, node, scope):
        self.visit(node.logic_concat_expr, scope)
        self.visit(node.comp_expr, scope)
    
    @visitor.when(CompExprNode)
    def visit(self, node, scope):
        self.visit(node.comp_expr, scope)
        self.visit(node.aritm_expr, scope)

    @visitor.when(AritmExprNode)
    def visit(self, node, scope):
        self.visit(node.aritm_expr, scope)
        self.visit(node.term, scope)

    @visitor.when(TermNode)
    def visit(self, node, scope):
        self.visit(node.term, scope)
        self.visit(node.pow_expr, scope)

    @visitor.when(PowExprNode)
    def visit(self, node, scope):
        self.visit(node.pow_expr, scope)
        self.visit(node.negative, scope)

    @visitor.when(NegativeNode)
    def visit(self, node, scope):
        self.visit(node.factor, scope)
    
    @visitor.when(FactorNode)
    def visit(self, node, scope):
        self.visit(node.expr, scope)
        self.visit(node.params_aux, scope)
        self.visit(node.expr2, scope)

    @visitor.when(LocNode)
    def visit(self, node, scope):
        if not scope.is_var_defined(node.id_):
            self.errors.append(f'Variable {node.id_} is not defined in current scope.')
        self.visit(node.args_in_par, scope)
    
    @visitor.when(ArgsNode)
    def visit(self, node, scope):
        self.visit(node.args_aux, scope)
    
    @visitor.when(ArgsAuxNode)
    def visit(self, node, scope):
        self.visit(node.args_aux, scope)
        self.visit(node.expr, scope)
    
    @visitor.when(ArgsInParNode)
    def visit(self, node, scope):
        self.visit(node.args, scope)
    

    


    


        

    

    

        



    



    ####################################
    
    # @visitor.when(ProgramNode)
    # def visit(self, node, scope=None):
    #     if scope is None:
    #         scope = Scope()
    #     for statement_node in node.statements:
    #         self.visit(statement_node, scope)
    #     return self.errors
    
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
    
    # @visitor.when(PrintExprNode)
    # def visit(self, node, scope):
    #     self.visit(node.expr, scope)
    
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
    
    # @visitor.when(BinaryNode)
    # def visit(self, node, scope):
    #     self.visit(node.left,scope)
    #     self.visit(node.right,scope)
