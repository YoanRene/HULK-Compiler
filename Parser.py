from Automata import *
from Grammar import *
from itertools import islice


def compute_local_first(firsts, alpha):
    first_set = firsts
    symbol_list = alpha
    result = ContainerSet()

    try:
        is_epsilon = symbol_list.is_epsilon
    except:
        is_epsilon = False

    if is_epsilon:
        result.set_epsilon()
    else:
        for symbol in symbol_list:
            first_of_symbol = first_set[symbol]
            result.update(first_of_symbol)
            if not first_of_symbol.contains_epsilon:
                break
        else:
            result.set_epsilon()

    return result

def compute_firsts(grammar):
    firsts = {}

    for terminal in grammar.terminals:
        firsts[terminal] = ContainerSet(terminal)

    for non_terminal in grammar.nonTerminals:
        firsts[non_terminal] = ContainerSet()

    has_changed = True

    while has_changed:
        has_changed = False

        for production in grammar.Productions:
            left_symbol = production.Left
            right_symbols = production.Right

            first_of_left = firsts[left_symbol]

            try:
                first_of_right = firsts[right_symbols]
            except:
                first_of_right = firsts[right_symbols] = ContainerSet()

            local_first_set = compute_local_first(firsts, right_symbols)

            has_changed |= first_of_right.hard_update(local_first_set)
            has_changed |= first_of_left.hard_update(local_first_set)

    return firsts

def compute_follows(grammar, firsts):
    first_set = firsts
    follows = {}
    has_changed = True
    epsilon_set = {}

    for non_terminal in grammar.nonTerminals:
        follows[non_terminal] = ContainerSet()

    follows[grammar.startSymbol] = ContainerSet(grammar.EOF)

    while has_changed:
        has_changed = False

        for production in grammar.Productions:
            left_symbol = production.Left
            right_symbols = production.Right

            result_set = follows[left_symbol]

            for i, symbol in enumerate(right_symbols):
                if symbol.IsNonTerminal:
                    follow_set = follows[symbol]

                    try:
                        first_beta = epsilon_set[(right_symbols, i)]
                    except:
                        first_beta = epsilon_set[(right_symbols, i)] = compute_local_first(first_set, right_symbols[i+1:])

                    has_changed |= follow_set.update(first_beta)

                    if first_beta.contains_epsilon:
                        has_changed |= follow_set.update(result_set)

    return follows

def build_parsing_table(grammar, firsts, follows):
    first_set = firsts
    follow_set = follows
    parsing_table = {}

    for production in grammar.Productions:
        left_symbol = production.Left
        right_symbols = production.Right

        for terminal in first_set[right_symbols]:
            try:
                parsing_table[(left_symbol, terminal)].append(production)
            except:
                parsing_table[(left_symbol, terminal)] = [production]

        if first_set[right_symbols].contains_epsilon:
            for terminal in follow_set[left_symbol]:
                try:
                    parsing_table[(left_symbol, terminal)].append(production)
                except:
                    parsing_table[(left_symbol, terminal)] = [production]

    return parsing_table

def metodo_predictivo_no_recursivo(G,M=None,firsts=None,follows=None):
 fi=firsts
 fo=follows
 if M is None:
  if fi is None:
   fi=compute_firsts(G)
  if fo is None:
   fo=compute_follows(G,fi)
  M=build_parsing_table(G,fi,fo)
 def m(w):
  V=[G.EOF,G.startSymbol]
  mm=0
  z=[]
  while True:
   g=V.pop()
   a=w[mm]
   if g.IsTerminal:
    if g==a:
     if g==G.EOF:
      break
     else:
      mm+=1
    else:
     print("Error. Aborting...")
     return None
   else:
    try:
     P=M[g,a][0]
     for i in range(len(P.Right)-1,-1,-1):
      V.append(P.Right[i])
     z.append(P)
    except:
     print("Error. Aborting...")
     return None
  return z
 return m

deprecated_metodo_predictivo_no_recursivo = metodo_predictivo_no_recursivo
def metodo_predictivo_no_recursivo(G, M=None, firsts=None, follows=None):
    parser = deprecated_metodo_predictivo_no_recursivo(G, M, firsts, follows)
    def updated(tokens):
        return parser([t.token_type for t in tokens])
    return updated

def multiline_formatter(state):
    return '\n'.join(str(item) for item in state)