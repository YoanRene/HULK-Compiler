from Grammar import *
from Automata import *
from Parser import *


class Node:
    def evaluate(self):
        raise NotImplementedError()

class AtomicNode(Node):
    def __init__(self, lex):
        self.lex = lex

class UnaryNode(Node):
    def __init__(self, node):
        self.node = node

    def evaluate(self):
        value = self.node.evaluate()
        return self.operate(value)

    @staticmethod
    def operate(value):
        raise NotImplementedError()

class BinaryNode(Node):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def evaluate(self):
        lvalue = self.left.evaluate()
        rvalue = self.right.evaluate()
        return self.operate(lvalue, rvalue)

    @staticmethod
    def operate(lvalue, rvalue):
        raise NotImplementedError()

def evaluate_parse(productions, tokens):
    if not productions or not tokens:
        return

    productions = iter(productions)
    tokens = iter(tokens)

    x = evaluate(next(productions), productions, tokens)
    assert isinstance(next(tokens).token_type, EOF)

    return x

def evaluate(production, productions, tokens, inherited_value=None):
    nonterminal, l = production
    attributes = production.attributes
    t = [None] * (len(l) + 1)
    k = [None] * (len(l) + 1)
    k[0] = inherited_value

    for i, R in enumerate(l, 1):
        if R.IsTerminal:
            assert k[i] is None
            t[i] = next(tokens).lex
        else:
            H = next(productions)
            assert R == H.Left
            P = attributes[i]
            if P is not None:
                k[i] = P(k, t)
            t[i] = evaluate(H, productions, tokens, k[i])

    P = attributes[0]
    return P(k, t) if P is not None else None

class EpsilonNode(AtomicNode):
    def evaluate(self):
        return DFA(states=1, finals=[0], transitions={})

class SymbolNode(AtomicNode):
    def evaluate(self):
        symbol = self.lex
        return DFA(states=2, finals=[1], transitions={(0, symbol): 1})

class ClosureNode(UnaryNode):
    @staticmethod
    def operate(value):
        return automata_closure(value)

class UnionNode(BinaryNode):
    @staticmethod
    def operate(lvalue, rvalue):
        return automata_union(lvalue, rvalue)

class ConcatNode(BinaryNode):
    @staticmethod
    def operate(lvalue, rvalue):
        return automata_concatenation(lvalue, rvalue)

def regex_tokenizer(text, grammar, skip_whitespaces=True):
    tokens = []
    token_map = {
        x: Token(x, grammar[x])
        for x in ['|', '*', '(', ')', 'ε']
    }
    escape=False
    for char in text:
        if escape:
            break
        if skip_whitespaces and char.isspace():
            continue
        try:
            if char == '/':
                if text[text.index(char) + 1] == '/':
                    token = Token(text[text.index(char) + 2], grammar['symbol'])
                    escape = True

            else:
                token = token_map[char]
            
        except KeyError:
            token = Token(char, grammar['symbol'])
        finally:
            tokens.append(token)
    tokens.append(Token('$', grammar.EOF))
    return tokens

def build_grammar():
    grammar = Grammar()
    E = grammar.NonTerminal('E', True)
    T, F, A, X, Y, Z = grammar.NonTerminals('T F A X Y Z')
    p, M, S, B, a, U = grammar.Terminals('| * ( ) symbol ε')
    E %= T + X, lambda h, s: s[2], None, lambda h, s: s[1]
    X %= p + E, lambda h, s: UnionNode(h[0], s[2])
    X %= grammar.Epsilon, lambda h, s: h[0]
    T %= F + Y, lambda h, s: s[2], None, lambda h, s: s[1]
    Y %= T, lambda h, s: ConcatNode(h[0], s[1])
    Y %= grammar.Epsilon, lambda h, s: h[0]
    F %= A + Z, lambda h, s: s[2], None, lambda h, s: s[1]
    Z %= M, lambda h, s: ClosureNode(h[0])
    Z %= grammar.Epsilon, lambda h, s: h[0]
    A %= a, lambda h, s: SymbolNode(s[1])
    A %= U, lambda h, s: EpsilonNode(s[1])
    A %= S + E + B, lambda h, s: s[2]
    return grammar

grammar = build_grammar()

L = metodo_predictivo_no_recursivo(grammar)

class Regex:
    def __init__(self, regex, skip_whitespaces=False):
        self.regex = regex
        self.automaton = self.build_automaton(regex)

    def __call__(self, text):
        return self.automaton.recognize(text)

    @staticmethod
    def build_automaton(regex, skip_whitespaces=False):
        tokens = regex_tokenizer(regex, grammar, skip_whitespaces=False)
        parse_tree = L(tokens)
        evaluated_tree = evaluate_parse(parse_tree, tokens)
        nfa = evaluated_tree.evaluate()
        dfa = nfa_to_dfa(nfa)
        minimized_dfa = automata_minimization(dfa)
        return minimized_dfa