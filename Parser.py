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


####Parser

# class ShiftReduceParser:
#  SHIFT='SHIFT'
#  REDUCE='REDUCE'
#  OK='OK'
#  def __init__(self,G,verbose=False):
#   self.G=G
#   self.verbose=verbose
#   self.action={}
#   self.goto={}
#   self._build_parsing_table()
#  def _build_parsing_table(self):
#   raise NotImplementedError()
#  def __call__(self,w,get_shift_reduce=False):
#   stack=[0]
#   cursor=0
#   output=[]
#   operations=[]
#   while True:
#    state=stack[-1]
#    lookahead=w[cursor]
#    if self.verbose:print(stack,'<---||--->',w[cursor:])
#    if(state,lookahead)not in self.action:
#     print((state,lookahead))
#     print("Error. Aborting...")
#     return None
#    action,tag=self.action[state,lookahead]
#    if action==self.SHIFT:
#     operations.append(self.SHIFT)
#     stack+=[lookahead,tag]
#     cursor+=1
#    elif action==self.REDUCE:
#     operations.append(self.REDUCE)
#     output.append(tag)
#     head,body=tag
#     for symbol in reversed(body):
#      stack.pop()
#      assert stack.pop()==symbol
#     state=stack[-1]
#     goto=self.goto[state,head]
#     stack+=[head,goto]
#    elif action==self.OK:
#     stack.pop()
#     assert stack.pop()==self.G.startSymbol
#     assert len(stack)==1
#     return output if not get_shift_reduce else(output,operations)
#    else:
#     raise Exception('Invalid action!!!')

# def expand(d,n):
#  y=d.NextSymbol
#  if y is None or not y.IsNonTerminal:
#   return[]
#  V=ContainerSet()
#  for E in d.Preview():
#   k=compute_local_first(n,E)
#   V.update(k)
#  assert not V.contains_epsilon
#  return[Item(prod,0,V)for prod in y.productions]
# def compress(A):
#  l={}
#  for d in A:
#   f=d.Center()
#   try:
#    V=l[f]
#   except KeyError:
#    l[f]=V=set()
#   V.update(d.lookaheads)
#  return{Item(x.production,x.pos,set(k))for x,k in l.items()}
# def closure_lr1(A,n):
#  H=ContainerSet(*A)
#  O=True
#  while O:
#   O=False
#   a=ContainerSet()
#   for d in H:
#    a.extend(expand(d,n))
#   O=H.update(a)
#  return compress(H)
# def goto_lr1(A,P,firsts=None,just_kernel=False):
#  assert just_kernel or firsts is not None,'`firsts` must be provided if `just_kernel=False`'
#  A=frozenset(d.NextItem()for d in A if d.NextSymbol==P)
#  return A if just_kernel else closure_lr1(A,firsts)

def multiline_formatter(state):
    return '\n'.join(str(item) for item in state)

# def build_LR1_automaton(G):
#  assert len(G.startSymbol.productions)==1,'Grammar must be augmented'
#  n=compute_firsts(G)
#  n[G.EOF]=ContainerSet(G.EOF)
#  I=G.startSymbol.productions[0]
#  o=Item(I,0,lookaheads=(G.EOF,))
#  t=frozenset([o])
#  H=closure_lr1(t,n)
#  r=State(frozenset(H),True)
#  v=[t]
#  h={t:r}
#  while v:
#   L=v.pop()
#   U=h[L]
#   for P in G.terminals+G.nonTerminals:
#    H=closure_lr1(L,n)
#    g=goto_lr1(H,P,just_kernel=True)
#    if not g:
#     continue
#    try:
#     w=h[g]
#    except KeyError:
#     H=closure_lr1(g,n)
#     w=h[g]=State(frozenset(H),True)
#     v.append(g)
#    U.add_transition(P.Name,w)
#  r.set_formatter(multiline_formatter)
#  return r

# class LR1Parser(ShiftReduceParser):
#  def _build_parsing_table(W):
#   G=W.G.AugmentedGrammar(True)
#   r=build_LR1_automaton(G)
#   for i,D in enumerate(r):
#    if W.verbose:print(i,'\t','\n\t '.join(str(x)for x in D.state),'\n')
#    D.idx=i
#   for D in r:
#    e=D.idx
#    for d in D.state:
#     if d.IsReduceItem:
#      p=d.production
#      if p.Left==G.startSymbol:
#       W._register(W.action,(e,G.EOF),(W.OK,None))
#      else:
#       for P in d.lookaheads:
#        W._register(W.action,(e,P),(W.REDUCE,p))
#     else:
#      P=d.NextSymbol
#      g=D.get(P.Name).idx
#      if P.IsTerminal:
#       W._register(W.action,(e,P),(W.SHIFT,g))
#      else:
#       W._register(W.goto,(e,P),g)
#  @staticmethod
#  def _register(F,K,N):
#   assert K not in F or F[K]==N,'Shift-Reduce or Reduce-Reduce conflict!!!'
#   F[K]=N
