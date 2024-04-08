import math
import random
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

    # def evaluate(self):
    #     try :
    #         return self.program.evaluate()
    #     except:
    #         pass
    #     try :
    #         return self.expr.evaluate()
    #     except:
    #         pass

class SumNode:
    def __init__(self,aritm_expr,term):
        self.aritm_expr=aritm_expr
        self.term=term
        self.ret_type = "num"
    
    # def evaluate(self):
    #     return self.aritm_expr.evaluate() + self.term.evaluate()

class MinusNode:
    def __init__(self,aritm_expr,term):
        self.aritm_expr=aritm_expr
        self.term=term
        self.ret_type = "num"
    
    def evaluate(self):
        return self.aritm_expr.evaluate() - self.term.evaluate()

class MultNode:
    def __init__(self,term,pow_expr):
        self.term=term
        self.pow_expr=pow_expr
        self.ret_type = "num"
    
    def evaluate(self):
        return self.term.evaluate() * self.pow_expr.evaluate()

class DivNode:
    def __init__(self,term,pow_expr):
        self.term=term
        self.pow_expr=pow_expr
        self.ret_type = "num"
    
    def evaluate(self):
        return self.term.evaluate() / self.pow_expr.evaluate()

class ModNode:
    def __init__(self,term,pow_expr):
        self.term=term
        self.pow_expr=pow_expr
        self.ret_type = "num"
    
    def evaluate(self):
        return self.term.evaluate() % self.pow_expr.evaluate()

class MathNode:
    def __init__(self,expr1,expr2):
        self.expr1=expr1
        self.expr2=expr2
        self.ret_type = "num"
    
    def evaluate(self):
        pass

class AndNode:
    def __init__(self,logic_concat_expr,comp_expr):
        self.logic_concat_expr=logic_concat_expr
        self.comp_expr=comp_expr
        self.ret_type = "bool"
    
    def evaluate(self):
        return self.logic_concat_expr.evaluate() and self.comp_expr.evaluate()

class OrNode:
    def __init__(self,logic_concat_expr,comp_expr):
        self.logic_concat_expr=logic_concat_expr
        self.comp_expr=comp_expr
        self.ret_type = "bool"
    
    def evaluate(self):
        return self.logic_concat_expr.evaluate() or self.comp_expr.evaluate()

class NotNode:
    def __init__(self,comp_expr):
        self.comp_expr=comp_expr
        self.ret_type = "bool"
    
    def evaluate(self):
        return not self.comp_expr.evaluate()

class BlockExprListNode:
    def __init__(self, block_expr_list,expr):
        self.block_expr_list = block_expr_list
        self.expr = expr

    def evaluate(self):
        # Implementación de la evaluación de la lista de bloques de expresiones
        pass

class LetOptionalNode:
    def __init__(self, let_optional):
        self.let_optional = let_optional

    def evaluate(self):
        # Implementación de la evaluación de la opción de let
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
    def __init__(self,params_aux, id_, id_extend):
        self.params_aux=params_aux
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
        self.ret_type = "str"

    def evaluate(self):
        # Implementación de la evaluación de la expresión de impresión
        pass

class LetExprNode:
    def __init__(self, decls,expr_body):
        self.decls = decls
        self.expr_body = expr_body
        self.ret_type = "let"

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
    def __init__(self, expr_elem, as_expr, is_expr):
        self.expr_elem = expr_elem
        self.as_expr = as_expr
        self.is_expr = is_expr

        if(is_expr):
            self.ret_type = "bool"
        else:
            try: 
                self.ret_type = as_expr.ret_type
            except:
                self.ret_type = expr_elem.ret_type

    def evaluate(self):
        # Implementación de la evaluación del elemento de expresión
        pass

class AsExprNode:
    def __init__(self, as_expr, logic_concat_expr):
        self.as_expr = as_expr
        self.logic_concat_expr = logic_concat_expr
        try:
            self.ret_type = logic_concat_expr.ret_type
        except:
            self.ret_type = as_expr.ret_type

    def evaluate(self):
        # Implementación de la evaluación de la expresión de conversión de tipo
        pass

class LogicConcatExprNode:
    def __init__(self, logic_concat_expr, comp_expr, arroba_type):
        self.logic_concat_expr = logic_concat_expr
        self.comp_expr = comp_expr
        self.arroba_type = arroba_type
        try:
            self.ret_type = comp_expr.ret_type
        except:
            self.ret_type = logic_concat_expr.ret_type

    def evaluate(self):
        if(self.arroba_type != None):
            if(self.arroba_type == "@"):
                return self.logic_concat_expr.evaluate() + self.comp_expr.evaluate()
            else:
                return self.logic_concat_expr.evaluate() + " " + self.comp_expr.evaluate()
        else:
            return self.comp_expr.evaluate()

class CompExprNode:
    def __init__(self, comp_expr, aritm_expr):
        self.comp_expr = comp_expr
        self.aritm_expr = aritm_expr
        try:
            self.ret_type = aritm_expr.ret_type ###################
        except:
            self.ret_type = comp_expr.ret_type

    def evaluate(self):
       return self.aritm_expr.evaluate()
        

class EqualsNode:
    def __init__(self, comp_expr, aritm_expr):
        self.comp_expr = comp_expr
        self.aritm_expr = aritm_expr
        self.ret_type = "bool"

    def evaluate(self):
        return self.comp_expr.evaluate() == self.aritm_expr.evaluate()

class NotEqualsNode:
    def __init__(self, comp_expr, aritm_expr):
        self.comp_expr = comp_expr
        self.aritm_expr = aritm_expr
        self.ret_type = "bool"

    def evaluate(self):
        # Implementación de la evaluación de la expresión de igualdad
        return self.comp_expr.evaluate() != self.aritm_expr.evaluate()

class LessNode:
    def __init__(self, comp_expr, aritm_expr):
        self.comp_expr = comp_expr
        self.aritm_expr = aritm_expr
        self.ret_type = "bool"

    def evaluate(self):
        return self.comp_expr.evaluate() < self.aritm_expr.evaluate()

class GreaterNode:
    def __init__(self, comp_expr, aritm_expr):
        self.comp_expr = comp_expr
        self.aritm_expr = aritm_expr
        self.ret_type = "bool"

    def evaluate(self):
        return self.comp_expr.evaluate() > self.aritm_expr.evaluate()

class LessEqualsNode:
    def __init__(self, comp_expr, aritm_expr):
        self.comp_expr = comp_expr
        self.aritm_expr = aritm_expr
        self.ret_type = "bool"

    def evaluate(self):
        return self.comp_expr.evaluate() <= self.aritm_expr.evaluate()

class GreaterEqualsNode:
    def __init__(self, comp_expr, aritm_expr):
        self.comp_expr = comp_expr
        self.aritm_expr = aritm_expr
        self.ret_type = "bool"

    def evaluate(self):
        return self.comp_expr.evaluate() >= self.aritm_expr.evaluate()

class AritmExprNode:
    def __init__(self, aritm_expr, term):
        self.aritm_expr = aritm_expr
        self.term = term
        self.ret_type = aritm_expr.ret_type #####################

    def evaluate(self):
        return self.aritm_expr.evaluate()

class TermNode:
    def __init__(self, term, pow_expr):
        self.term = term
        self.pow_expr = pow_expr
        try:
            self.ret_type = pow_expr.ret_type
        except:
            self.ret_type = term.ret_type

    def evaluate(self):
        return self.term.evaluate()

class PowExprNode:
    def __init__(self, pow_expr, negative):
        self.pow_expr = pow_expr
        self.negative = negative
        try: 
            self.ret_type = negative.ret_type
        except:
            self.ret_type = pow_expr.ret_type

    def evaluate(self):
        if(self.pow_expr != None):
            return self.pow_expr.evaluate() ** self.negative.evaluate()
        else:
            return self.negative.evaluate()

class NegativeNode:
    def __init__(self, factor, is_negative):
        self.factor = factor
        self.is_negative = is_negative
        self.ret_type = factor.ret_type

    def evaluate(self):
        if(self.is_negative):
            return -self.factor.evaluate()
        else:
            return self.factor.evaluate()

class FactorNode:
    def __init__(self, expr, params_aux,expr2):
        self.expr = expr
        self.params_aux = params_aux
        self.expr2 = expr2
        self.ret_type = expr.ret_type

    def evaluate(self):
        # Implementación de la evaluación del factor de expresión
        pass

class LocNode:
    def __init__(self, loc, id_, args_in_par):
        self.loc = loc
        self.id_ = id_
        self.args_in_par = args_in_par
        self.ret_type = "str"

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
    def __init__(self, args, is_args_in_par):
        self.args = args
        self.is_args_in_par = is_args_in_par

    def evaluate(self):
        # Implementación de la evaluación de los argumentos entre paréntesis
        pass

class NumNode: 
    def __init__(self, value,value2, math_func):
        self.value= value
        self.value2= value2
        self.math_func = math_func
        self.ret_type = "num"


    def evaluate(self):
        if(self.math_func != None):
            if(self.math_func == "sin"):
                return math.sin(int(self.value))
            elif(self.math_func == "cos"):
                return math.cos(int(self.value))
            elif(self.math_func == "sqrt"):
                return math.sqrt(int(self.value))
            elif(self.math_func == "log"):
                return math.log(int(self.value),int(self.value2))
            elif(self.math_func == "exp"):
                return math.exp(int(self.value))
            elif(self.math_func == "rand"):
                return random.randint()####
        else: 
            return int(self.value)
        
class BoolNode:
    def __init__(self, value):
        self.value= value
        self.ret_type = "bool"

    def evaluate(self):
        # Implementación de la evaluación del booleano
        pass

class StrNode:
    def __init__(self, value):
        self.value= value
        self.ret_type = "str"

    def evaluate(self):
        return self.value

class VectorNode:
    def __init__(self, expr, params_aux, expr2):
        self.expr = expr
        self.params_aux = params_aux
        self.expr2 = expr2
        self.ret_type = "vector"

    def evaluate(self):
        # Implementación de la evaluación del vector
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
    
    @visitor.when(SumNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\__SumNode <expr> + <expr>'
        left = self.visit(node.aritm_expr, tabs + 1)
        right = self.visit(node.term, tabs + 1)
        return f'{ans}\n{left}\n{right}'
    
    @visitor.when(MinusNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\__MinusNode <expr> - <expr>'
        left = self.visit(node.aritm_expr, tabs + 1)
        right = self.visit(node.term, tabs + 1)
        if(right !=[] and right!=None):
            return f'{ans}\n{left}\n{right}'
        else:
            return f'{ans}\n{left}'
    
    @visitor.when(MultNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\__MultNode <expr> * <expr>'
        left = self.visit(node.term, tabs + 1)
        right = self.visit(node.pow_expr, tabs + 1)
        return f'{ans}\n{left}\n{right}'
    
    @visitor.when(DivNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\__DivNode <expr> / <expr>'
        left = self.visit(node.term, tabs + 1)
        right = self.visit(node.pow_expr, tabs + 1)
        return f'{ans}\n{left}\n{right}'
    
    @visitor.when(ModNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\__ModNode <expr> % <expr>'
        left = self.visit(node.term, tabs + 1)
        right = self.visit(node.pow_expr, tabs + 1)
        return f'{ans}\n{left}\n{right}'
    
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
        id = node.id_
        params = self.visit(node.params, tabs + 1)
        id_extend = self.visit(node.id_extend, tabs + 1)
        body = self.visit(node.body, tabs + 1)

        if(id_extend !=[] and id_extend != None):
            if id != None :
                return f'{ans}\n{id}\n{params}\n{id_extend}\n{body}'
            else:
                return f'{ans}\n{params}\n{id_extend}\n{body}'
        elif id != None:
            return f'{ans}\n{id}\n{params}\n{body}'
        else:
            return f'{ans}\n{params}\n{body}'

    
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
        expr = self.visit(node.expr, tabs + 1)
        return f'{ans}\n{expr}'
    
    @visitor.when(ParamsAuxNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\__ParamsAuxNode <id> :'
        id = node.id_
        id_extend = self.visit(node.id_extend, tabs + 1)
        if(id_extend != [] and id_extend != None):
            return f'{ans}\n{id},{id_extend}'
        else:
            return f'{ans} {id}'
    
    @visitor.when(ParamsNode) #######################
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\__ParamsNode <id> : <type>'
        string=""
        for param in node.params_aux:
            x= self.visit(param, tabs + 1)
            if x != []:
                string += self.visit(param, tabs + 1)+","
        if(string != ""):
            params_aux = string[:-1]
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
        if (node.id_!=None):
            return f'{ans}\n{node.id_}'
    
    @visitor.when(ExprElemNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\__ExprElemNode <expr> <expr_elem>'
        expr_elem = self.visit(node.expr_elem, tabs + 1)
        as_expr = self.visit(node.as_expr, tabs + 1)
        if(expr_elem != [] and expr_elem != None):
            if(as_expr != [] and as_expr != None):
                return f'{ans}\n{expr_elem}\n{as_expr}'
            return f'{ans}\n{expr_elem}'
        elif as_expr != [] and as_expr != None:
            return f'{ans}\n{as_expr}'
    
    @visitor.when(AsExprNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\__AsExprNode <expr>'
        as_expr = self.visit(node.as_expr, tabs + 1)
        logic_concat_expr = self.visit(node.logic_concat_expr, tabs + 1)

        if(as_expr != [] and as_expr != None):
            if (logic_concat_expr != [] and logic_concat_expr != None):
                return f'{ans}\n{as_expr}\n{logic_concat_expr}'
            return f'{ans}\n{as_expr}'
        elif logic_concat_expr != [] and logic_concat_expr != None:
            return f'{ans}\n{logic_concat_expr}'
    
    @visitor.when(LogicConcatExprNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\__LogicConcatExprNode <expr> <logic_concat_expr>'
        logic_concat_expr = self.visit(node.logic_concat_expr, tabs + 1)
        comp_expr = self.visit(node.comp_expr, tabs + 1)
        if(logic_concat_expr != [] and logic_concat_expr != None):
            if (comp_expr != [] and comp_expr != None):
                return f'{ans}\n{logic_concat_expr}\n{comp_expr}'
            return f'{ans}\n{logic_concat_expr}'
        elif comp_expr != [] and comp_expr != None:
            return f'{ans}\n{comp_expr}'
    
    @visitor.when(CompExprNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\__CompExprNode <expr> <comp_expr>'
        comp_expr = self.visit(node.comp_expr, tabs + 1)
        aritm_expr = self.visit(node.aritm_expr, tabs + 1)
        if(comp_expr != [] and comp_expr != None):
            if (aritm_expr != [] and aritm_expr != None):
                return f'{ans}\n{comp_expr}\n{aritm_expr}'
            return f'{ans}\n{comp_expr}'
        elif aritm_expr != [] and aritm_expr != None:
            return f'{ans}\n{aritm_expr}'
    
    @visitor.when(AritmExprNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\__AritmExprNode <expr> <aritm_expr>'
        aritm_expr = self.visit(node.aritm_expr, tabs + 1)
        term = self.visit(node.term, tabs + 1)

        if(aritm_expr != [] and aritm_expr != None):
            if (term != [] and term != None):
                return f'{ans}\n{aritm_expr}\n{term}'
            return f'{ans}\n{aritm_expr}'
        elif term != [] and term != None:
            return f'{ans}\n{term}'
    
    @visitor.when(TermNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\__TermNode <expr> <term>'
        term = self.visit(node.term, tabs + 1)
        pow_expr = self.visit(node.pow_expr, tabs + 1)
        if( pow_expr != [] and pow_expr != None):
            if(term != [] and term != None):
                return f'{ans}\n{term}\n{pow_expr}'
            return f'{ans}\n{pow_expr}'
        elif term != [] and term != None:
            return f'{ans}\n{term}'
    
    @visitor.when(PowExprNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\__PowExprNode <expr> <pow_expr>'
        pow_expr = self.visit(node.pow_expr, tabs + 1)
        negative = self.visit(node.negative, tabs + 1)
        if(negative!=[] and negative!=None):
            return f'{ans}\n{pow_expr}\n{negative}'
        elif pow_expr != [] and pow_expr != None:
            return f'{ans}\n{pow_expr}'
    
    @visitor.when(NegativeNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\__NegativeNode <expr>'
        factor = self.visit(node.factor, tabs + 1)
        if(factor != [] and factor != None):
            return f'{ans}\n{factor}'
        
    
    @visitor.when(FactorNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\__FactorNode'
        expr = self.visit(node.expr, tabs + 1)
        # params_aux = self.visit(node.params_aux, tabs + 1)
        # expr2 = self.visit(node.expr2, tabs + 1)
        if(expr != [] and expr != None):
            return f'{ans}\n{expr}'
    
    @visitor.when(LocNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\__LocNode <expr>'
        loc = self.visit(node.loc, tabs + 1)
        id= self.visit(node.id_, tabs + 1)
        args_in_par = self.visit(node.args_in_par, tabs + 1)
        if loc != []:
            if id != []:
                if args_in_par != []:
                    return f'{ans}\n{loc}\n{id}\n{args_in_par}'
                else:
                    return f'{ans}\n{loc}\n{args_in_par}'
            return f'{ans}\n{loc}'
        elif id != []:
            if args_in_par != []:
                return f'{ans}\n{id}\n{args_in_par}'
            return f'{ans}\n{args_in_par}'
        elif args_in_par != [] and args_in_par != None:
            return f'{ans}\n{args_in_par}'
    
    @visitor.when(ArgsAuxNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\__ArgsAuxNode <expr> <args_aux>'
        args_aux = self.visit(node.args_aux, tabs + 1)
        expr = self.visit(node.expr, tabs + 1)
        if(expr != []):
            return f'{ans}\n{args_aux}\n{expr}'
        else:
            return f'{ans}\n{args_aux}'
    
    @visitor.when(ArgsNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\__ArgsNode <expr>'
        args_aux = self.visit(node.args_aux, tabs + 1)

        return f'{ans}\n{args_aux}'
    
    @visitor.when(ArgsInParNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\__ArgsInParNode <expr>'
        args = self.visit(node.args, tabs + 1)
        if(args != []):
            return f'{ans}\n{args}'
    
    @visitor.when(NumNode)
    def visit(self, node, tabs=0):
        if(node.math_func != None):
            value=self.visit(node.value, tabs + 1)
            if value != [] and value != None:
                return '\t' * tabs + f'\\__NumNode: {node.math_func} {value}'
            return '\t' * tabs + f'\\__NumNode: {node.math_func}'
        return '\t' * tabs + f'\\__NumNode: {node.value}'
    
    @visitor.when(BoolNode)
    def visit(self, node, tabs=0):
        return '\t' * tabs + f'\\__BoolNode: {node.value}'
    
    @visitor.when(StrNode)
    def visit(self, node, tabs=0):
        return '\t' * tabs + f'\\__StrNode: {node.value}'
    

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

        #las nuevas para la evaluacion
        self.variables = {}
        self.variables_extends = {}
        self.functions = {}
        self.functions_extends = {}
        self.protocols = []
        self.types = []

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
    
    #funciones nuevas
    def insert_variable(self, var_name, var_value):
        self.variables[var_name] = var_value

    def get_variable(self, var_name):
        return self.variables[var_name]
    
    def insert_function(self, fun_name, fun_params, fun_extends, fun_body):
        self.functions[fun_name] = (fun_params, fun_extends, fun_body)
        self.functions_extends[fun_name] = fun_extends
    
    def get_function(self, fun_name):
        return self.functions[fun_name]
    
    def insert_type(self, type_name, type_params, type_inherits, type_decls_met):
        self.types[type_name] = (type_params, type_inherits, type_decls_met)
    
    def get_type(self, type_name):
        return self.types[type_name]

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
        if not scope.define_function(node.id_, node.params.params_aux):###########
            self.errors.append(f'Function {node.id} is already defined in current scope.')
        inner_scope = scope.create_child_scope()
        for param in node.params.params_aux:
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
        self.visit(node.expr, scope)

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
        try:
            if (node.expr.ret_type == "bool"):
                self.visit(node.expr, scope)
            else:
                self.errors.append(f'While condition must be a boolean expression.')
        except:
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
        try:
            if (node.expr.ret_type == "bool"):
                
                self.visit(node.expr, scope)
            else:
                self.errors.append(f'If condition must be a boolean expression.')
        except:
            self.errors.append(f'If condition must be a boolean expression.')
        inner_scope = scope.create_child_scope()
        self.visit(node.expr_body, inner_scope)
        self.visit(node.elif_expr, inner_scope)

    @visitor.when(ElifExprNode)#######
    def visit(self, node, scope):
        if node.expr is not None:
            try:
                #generame un if de si node.expr es una instancia de LogicConcatExprNode o un CompExprNode
                if (node.expr.ret_type == "bool"):
                    self.visit(node.expr, scope)
                else:
                    self.errors.append(f'Elif condition must be a boolean expression.')
            except:
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
        # if not scope.define_variable(node.id_):
        #     self.errors.append(f'Variable {node.id_} is already defined in current scope.')
        if scope.is_var_defined(node.id_extend.id_):###########################is type defined
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

    @visitor.when(AndNode)
    def visit(self, node, scope):
        self.visit(node.logic_concat_expr, scope)
        self.visit(node.comp_expr, scope)

    @visitor.when(OrNode)
    def visit(self, node, scope):
        self.visit(node.logic_concat_expr, scope)
        self.visit(node.comp_expr, scope)

    @visitor.when(NotNode)
    def visit(self, node, scope):
        #self.visit(node.logic_concat_expr, scope)
        self.visit(node.comp_expr, scope)

    @visitor.when(AritmExprNode)
    def visit(self, node, scope):
        # if(not(recursivity(node.aritm_expr)== recursivity(node.term))):
        #     self.errors.append(f'Incompatible types in arithmetical expression.')
        self.visit(node.aritm_expr, scope)
        self.visit(node.term, scope)


    @visitor.when(SumNode)
    def visit(self, node, scope):
        #type_1 = findType(node.aritm_expr)
        #type_2 = findType(node.term)
        type_1 = node.aritm_expr.ret_type
        type_2 = node.term.ret_type
        if(not(type_1 == type_2) and type_1 != 'str' and type_2 != 'str'):
            self.errors.append(f'Incompatible types in arithmetical expression.')
        self.visit(node.aritm_expr, scope)
        self.visit(node.term, scope)

    @visitor.when(MinusNode)
    def visit(self, node, scope):
        #type_1 = findType(node.aritm_expr)
        #type_2 = findType(node.term)
        type_1 = node.aritm_expr.ret_type
        type_2 = node.term.ret_type
        if(not(type_1 == type_2) and type_1 != 'str' and type_2 != 'str'):
            self.errors.append(f'Incompatible types in arithmetical expression.')
        self.visit(node.aritm_expr, scope)
        self.visit(node.term, scope)

    @visitor.when(DivNode)
    def visit(self, node, scope):
        #type_1 = findType(node.pow_expr)
        #type_2 = findType(node.term)
        type_1 = node.pow_expr.ret_type
        type_2 = node.term.ret_type
        if(not(type_1 == type_2) and type_1 != 'str' and type_2 != 'str'):
            self.errors.append(f'Incompatible types in arithmetical expression.')
        self.visit(node.pow_expr, scope)
        self.visit(node.term, scope)

    @visitor.when(MultNode)
    def visit(self, node, scope):
        #type_1 = findType(node.pow_expr)
        #type_2 = findType(node.term)
        type_1 = node.pow_expr.ret_type
        type_2 = node.term.ret_type
        if(not(type_1 == type_2) and type_1 != 'str' and type_2 != 'str'):
            self.errors.append(f'Incompatible types in arithmetical expression.')
        self.visit(node.pow_expr, scope)
        self.visit(node.term, scope)
    
    @visitor.when(ModNode)
    def visit(self, node, scope):
        #type_1 = findType(node.aritm_expr)
        #type_2 = findType(node.term)
        type_1 = node.pow_expr.ret_type
        type_2 = node.term.ret_type
        if(not(type_1 == type_2) and type_1 != 'str' and type_2 != 'str'):
            self.errors.append(f'Incompatible types in arithmetical expression.')
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

    @visitor.when(VectorNode)
    def visit(self, node, scope):
        self.visit(node.expr, scope)
        self.visit(node.params_aux, scope)
        self.visit(node.expr2, scope)


    @visitor.when(LocNode)
    def visit(self, node, scope):
        # if not scope.is_var_defined(node.id_):
        #     self.errors.append(f'Variable {node.id_} is not defined in current scope.')
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




def findType(node):

    try:
        return findType(node.expr_elem)
    except:
        pass

    try:
        return findType(node.as_expr)
    except:
        pass

    try:
        return findType(node.logic_concat_expr)
    except:
        pass

    try:
        return findType(node.comp_expr)
    except:
        pass

    try:
        return findType(node.aritm_expr)
    except:
        pass

    try:
        return findType(node.term)
    except:
        pass

    try:
        return findType(node.pow_expr)
    except:
        pass

    try:
        return findType(node.negative)
    except:
        pass

    try:
        return findType(node.factor)
    except:
        pass

    try:
        return findType(node.loc)####
    except:
        pass

    try:
        return findType(node.expr)
    except:
        pass

    return node.__class__.__name__

    # try:
    #     if node.term.pow_expr.factor.__class__.__name__== "NumNode" or node.term.pow_expr.factor.__class__.__name__== "MathNode":
    #         return "num"
    # except:
    #     pass
    # try :
    #     if node.pow_expr.factor.__class__.__name__== "NumNode" or node.pow_expr.factor.__class__.__name__== "MathNode":
    #         return "num"
    # except:
    #     pass
    # try:
    #     if node.aritm_expr.term.pow_expr.factor.__class__.__name__== "NumNode" or node.aritm_expr.term.pow_expr.factor.__class__.__name__== "MathNode":
    #         return "num"
    # except:
    #     pass
    # try :
    #     if node.aritm_expr.term.__class__.__name__== "MultNode" or node.aritm_expr.term.__class__.__name__== "DivNode"or node.aritm_expr.term.__class__.__name__== "ModNode":
    #         return "num"
    # except:
    #     pass

#region Evaluate

class SemanticCheckerEvaluate(object):
    def __init__(self):
        #self.errors = []
        self.results = []
    
    @visitor.on('node')
    def visit(self, node, scope):
        pass
    
    @visitor.when(ProgramNode)
    def visit(self, node, scope=None):
        if scope is None:
            scope = Scope()
        try :
            x = self.visit(node.program, scope)
            if x != None:
                self.results.append(x)
        except:
            pass
        try :
            res = self.visit(node.expr, scope)
            if res != None:
                self.results.append(res)
                return res
        except:
            pass
    
    @visitor.when(ExprNode)
    def visit(self, node, scope):
        self.visit(node.expr_elem, scope)
        self.visit(node.expr, scope)

    @visitor.when(FunctionStatNode)#########################################################
    def visit(self, node, scope):
        scope.insert_function(node.id_, node.params, node.id_extend, node.body)######### no se si es node.params.paramsa_aux o como esta puesto


    @visitor.when(TypeStatNode)##############################################################
    def visit(self, node, scope):
        scope.insert_type(node.id_, node.params_in_par.params, node.inherit, node.decls_methods_semi)##########
        return
        
    @visitor.when(ProtocolStatNode)#############################################################
    def visit(self, node, scope):
        pass

    @visitor.when(MethodProtocolNode)############################################################
    def visit(self, node, scope):
        pass
    
    @visitor.when(MethodNode)################################################################
    def visit(self, node, scope):
        pass

    @visitor.when(ExtendsExprNode)###############################################################
    def visit(self, node, scope):
        pass

    @visitor.when(InheritsExprNode)############################################################
    def visit(self, node, scope):
        pass##################################################

    @visitor.when(BodyNode)####################################################################
    def visit(self, node, scope):
        return self.visit(node.expr, scope)

    @visitor.when(ParamsNode)
    def visit(self, node, scope):
        return self.visit(node.params_aux, scope)

    @visitor.when(ParamsAuxNode)
    def visit(self, node, scope):
        pass
        
    @visitor.when(ParamsInParNode)
    def visit(self, node, scope):
        pass

    @visitor.when(InstExprNode)
    def visit(self, node, scope):
        pass
    
    @visitor.when(ArrayExprNode)
    def visit(self, node, scope):
        pass

    @visitor.when(PrintExprNode)
    def visit(self, node, scope):
        return str(self.visit(node.expr, scope))

    @visitor.when(LetExprNode)
    def visit(self, node, scope):
        #inner_scope = scope.create_child_scope()
        for decl in node.decls:##########################3
            scope.variables[decl.id_] = self.visit(decl.expr, scope)
            if(decl.id_extend.id_ != None):
                scope.variables_extends[decl.id_] = decl.id_extend.id_ 
        
        return self.visit(node.expr_body, scope)

    @visitor.when(DestrExprNode)
    def visit(self, node, scope):

        scope.variables[node.loc.id_] = self.visit(node.expr, scope)


    @visitor.when(WhileExprNode)
    def visit(self, node, scope):
        while(node.expr):
            self.visit(node.expr_body, scope)

    @visitor.when(ForExprNode)
    def visit(self, node, scope):
        pass
    
    @visitor.when(IfExprNode)
    def visit(self, node, scope):
        if(self.visit(node.expr, scope)):
            return self.visit(node.expr_body, scope)
        else:
            return self.visit(node.elif_expr, scope)
        

    @visitor.when(ElifExprNode)#######
    def visit(self, node, scope):
        if(self.visit(node.expr, scope)):
            return self.visit(node.expr_body, scope)
        return self.visit(node.elif_expr, scope)
        

    @visitor.when(ElseExprNode)
    def visit(self, node, scope):
        return self.visit(node.expr_body, scope)

    @visitor.when(DeclNode)
    def visit(self, node, scope):
        pass

    @visitor.when(DeclsNode)
    def visit(self, node, scope):
        pass
    
    @visitor.when(ExprBodyNode)
    def visit(self, node, scope):
        return self.visit(node.expr, scope)
    
    @visitor.when(ExprListSemiNode)
    def visit(self, node, scope):
        ret_value =[]
        if(node.expr_list_semi != None):
            ret_value.append(self.visit(node.expr_list_semi, scope))
        if(node.expr != None):
            ret_value.append(self.visit(node.expr, scope))
        return ret_value

    @visitor.when(IdExtendNode) ###################
    def visit(self, node, scope):
        pass
    
    @visitor.when(ExprElemNode)
    def visit(self, node, scope):
        if(node.is_expr):
            if(node.expr_elem.ret_type == node.as_expr.ret_type):
                return True
            elif(node.expr_elem in scope.variables_extends.keys() and scope.variables_extends[node.expr_elem] == node.as_expr.ret_type):            
                return True
            else:
                return False
        else:
            return self.visit(node.expr_elem, scope)

    @visitor.when(AsExprNode)
    def visit(self, node, scope):
        return self.visit(node.as_expr, scope)

    @visitor.when(LogicConcatExprNode)
    def visit(self, node, scope):
        if(node.arroba_type == "@"):
            return str(self.visit(node.logic_concat_expr, scope)) + str(self.visit(node.comp_expr, scope))
        elif(node.arroba_type == "@@"):
            return str(self.visit(node.logic_concat_expr, scope)) + " " + str(self.visit(node.comp_expr, scope))
        else:
            return self.visit(node.logic_concat_expr, scope)
    
    @visitor.when(CompExprNode)
    def visit(self, node, scope):
        return self.visit(node.comp_expr, scope)

    @visitor.when(EqualsNode)
    def visit(self, node, scope):
        return self.visit(node.comp_expr, scope) == self.visit(node.aritm_expr, scope)
    
    @visitor.when(NotEqualsNode)
    def visit(self, node, scope):
        return self.visit(node.comp_expr, scope) != self.visit(node.aritm_expr, scope)
    
    @visitor.when(LessNode)
    def visit(self, node, scope):
        return self.visit(node.comp_expr, scope) < self.visit(node.aritm_expr, scope)
    
    @visitor.when(LessEqualsNode)
    def visit(self, node, scope):
        return self.visit(node.comp_expr, scope) <= self.visit(node.aritm_expr, scope)
    
    @visitor.when(GreaterNode)
    def visit(self, node, scope):
        return self.visit(node.comp_expr, scope) > self.visit(node.aritm_expr, scope)
    
    @visitor.when(GreaterEqualsNode)
    def visit(self, node, scope):
        return self.visit(node.comp_expr, scope) >= self.visit(node.aritm_expr, scope)
    

            
    @visitor.when(AndNode)
    def visit(self, node, scope):
        return self.visit(node.logic_concat_expr, scope) and self.visit(node.comp_expr, scope)

    @visitor.when(OrNode)
    def visit(self, node, scope):
        return self.visit(node.logic_concat_expr, scope) or self.visit(node.comp_expr, scope)

    @visitor.when(NotNode)
    def visit(self, node, scope):
        return not self.visit(node.comp_expr, scope)

    @visitor.when(AritmExprNode)
    def visit(self, node, scope):
        return self.visit(node.aritm_expr, scope)


    @visitor.when(SumNode)
    def visit(self, node, scope):
        return self.visit(node.aritm_expr,scope) + self.visit(node.term,scope)

    @visitor.when(MinusNode)
    def visit(self, node, scope):
        return self.visit(node.aritm_expr,scope) - self.visit(node.term,scope)

    @visitor.when(DivNode)
    def visit(self, node, scope):
        return self.visit(node.term,scope) / self.visit(node.pow_expr,scope)

    @visitor.when(MultNode)
    def visit(self, node, scope):
        return self.visit(node.term,scope) * self.visit(node.pow_expr,scope)
    
    @visitor.when(ModNode)
    def visit(self, node, scope):
        return self.visit(node.term,scope) % self.visit(node.pow_expr,scope)
    

    @visitor.when(TermNode)
    def visit(self, node, scope):
        return self.visit(node.term, scope)

    @visitor.when(PowExprNode)
    def visit(self, node, scope):
        if(node.negative is not None):
            return self.visit(node.pow_expr, scope) ** self.visit(node.negative, scope)
        
        else:
            return self.visit(node.pow_expr, scope)

    @visitor.when(NegativeNode)
    def visit(self, node, scope):
        if(node.is_negative):
            return -self.visit(node.negative, scope)
        else:
            return self.visit(node.factor, scope)
    
    @visitor.when(FactorNode)
    def visit(self, node, scope):
        return self.visit(node.expr, scope)
    

    @visitor.when(LocNode) #########Este tampoco##################################
    def visit(self, node, scope):
        if(node.loc is None):
            if(not node.args_in_par.is_args_in_par):####################
                return scope.get_variable(node.id_)
            else:
                pass
        else:
            pass
    
    @visitor.when(ArgsNode) ############# ?
    def visit(self, node, scope):
        pass
    
    @visitor.when(ArgsAuxNode) ########## ?
    def visit(self, node, scope):
        pass
    
    @visitor.when(ArgsInParNode)
    def visit(self, node, scope):
        return self.visit(node.args, scope)
    
    @visitor.when(NumNode)
    def visit(self, node, scope):
        if(node.math_func != None):
            if(node.math_func == "sin"):
                return math.sin(int(node.value))
            elif(node.math_func == "cos"):
                return math.cos(int(node.value))
            elif(node.math_func == "sqrt"):
                return math.sqrt(int(node.value))
            elif(node.math_func == "log"):
                return math.log(int(node.value),int(node.value2))
            elif(node.math_func == "exp"):
                return math.exp(int(node.value))
            elif(node.math_func == "rand"):
                return random.randint()####
        else: 
            return int(node.value)
    
    #@visitor.when(BoolNode)

    @visitor.when(StrNode)
    def visit(self, node, scope):
        return node.value

#endregion