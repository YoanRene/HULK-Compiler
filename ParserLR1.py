from Automata import *
from Parser import *

class ShiftReduceParser:
    SHIFT = 'SHIFT'
    REDUCE = 'REDUCE'
    OK = 'OK'
    
    def __init__(self, G, verbose=False):
        self.G = G
        self.verbose = verbose
        self.action = {}
        self.goto = {}
        self._build_parsing_table()
    
    def _build_parsing_table(self):
        raise NotImplementedError()

    def __call__(self, w, lines, get_shift_reduce=False):
        stack = [ 0 ]
        cursor = 0
        output = []
        operations=[]
        
        while True:
            state = stack[-1]
            lookahead = w[cursor]
            if self.verbose: print(stack, '<---||--->', w[cursor:])
                
            #(Detect error)
            try:
                self.action[state, lookahead.Name]
            except:
                assert False, f"Failed to parse in line {lines[cursor]}"

            action, tag = self.action[state, lookahead.Name]
            #(Shift case)
            if action == self.SHIFT:
                operations.append(self.SHIFT)
                cursor -= -1
                stack.append(tag)
                continue
            #(Reduce case)
            if action == self.REDUCE:
                operations.append(self.REDUCE)
                if not tag.Right.IsEpsilon:
                    for i in range(len(tag.Right)):
                        stack.pop()
                new_state = stack.pop()
                stack.append(new_state)
                stack.append(self.goto[new_state, tag.Left.Name])
                output.append(tag)
                continue
            #(OK case)
            if action == self.OK:
                #output.append(tag)
                return output if not get_shift_reduce else(output,operations)
            #(Invalid case)
            return None        


def compress(items):
    centers = {}

    for item in items:
        center = item.Center()
        try:
            lookaheads = centers[center]
        except KeyError:
            centers[center] = lookaheads = set()
        lookaheads.update(item.lookaheads)
    
    return { Item(x.production, x.pos, set(lookahead)) for x, lookahead in centers.items() }

def expand(G, item, firsts):
    next_symbol = item.NextSymbol
    if next_symbol is None or not next_symbol.IsNonTerminal:
        return []
    
    lookaheads = ContainerSet()
    #(Compute lookahead for child items)
    new_items = []
    previews = item.Preview()
    for preview in previews:
        sentence = G.Epsilon
        for symbol in preview:
            sentence = sentence + symbol
        try:
            prev_first = firsts[sentence]
        except KeyError:
            prev_first = firsts[sentence] = compute_local_first(firsts, preview)
        
        lookaheads.update(prev_first)
    
    assert not lookaheads.contains_epsilon
    #(Build and return child items)
    for prod in next_symbol.productions:
            new_item = Item(prod, 0, lookaheads = lookaheads)
            new_items.append(new_item)
    return new_items


def closure_lr1(G, items, firsts):
    closure = ContainerSet(*items)
    
    changed = True
    while changed:
        changed = False
        
        new_items = ContainerSet()
        for item in closure:
            new_items.update(ContainerSet(*expand(G , item, firsts)))

        changed = closure.update(new_items)
        
    return compress(closure)

def goto_lr1(G, items, symbol, firsts=None, just_kernel=False):
    assert just_kernel or firsts is not None, '`firsts` must be provided if `just_kernel=False`'
    items = frozenset(item.NextItem() for item in items if item.NextSymbol == symbol)
    return items if just_kernel else closure_lr1(G, items, firsts)


def build_LR1_automaton(G):
    assert len(G.startSymbol.productions) == 1, 'Grammar must be augmented'
    
    firsts = compute_firsts(G)
    firsts[G.EOF] = ContainerSet(G.EOF)
    
    start_production = G.startSymbol.productions[0]
    start_item = Item(start_production, 0, lookaheads=(G.EOF,))
    start = frozenset([start_item])
    
    closure = closure_lr1(G, start, firsts)
    automaton = State(frozenset(closure), True)
    
    pending = [ start ]
    visited = { start: automaton }
    
    while pending:
        current = pending.pop()
        current_state = visited[current]
        for symbol in G.terminals + G.nonTerminals:
            #(Get/Build `next_state`)
            closure_current = closure_lr1(G ,current, firsts)
            goto = goto_lr1(G, closure_current, symbol, just_kernel=True)
            if len(goto) == 0:
                continue
            try:
                next_state = visited[goto]
            except KeyError:
                next_closure = closure_lr1(G ,goto, firsts)
                visited[goto] = next_state = State(frozenset(next_closure), True)
                pending.append(goto)
            current_state.add_transition(symbol.Name, next_state)
    
    automaton.set_formatter(multiline_formatter)
    return automaton


class LR1Parser(ShiftReduceParser):
    def _build_parsing_table(self):
        G = self.G.AugmentedGrammar(True)
        
        automaton = build_LR1_automaton(G)
        for i, node in enumerate(automaton):
            if self.verbose: print(i, '\t', '\n\t '.join(str(x) for x in node.state), '\n')
            node.idx = i

        prodOk = G.startSymbol.productions[0]
        posOk = len(prodOk.Right)

        for node in automaton:
            idx = node.idx
            for item in node.state:
                if item.IsReduceItem:
                    if item.production == prodOk and posOk == item.pos and G.EOF in item.lookaheads:
                        self._register(self.action, (idx, G.EOF.Name),(self.OK, 1))
                        continue
                    
                    for lookahead in item.lookaheads:
                        self._register(self.action, (idx, lookahead.Name), (self.REDUCE, item.production))
                        
                else:
                    if item.NextSymbol.IsTerminal:
                        self._register(self.action, (idx, item.NextSymbol.Name), (self.SHIFT, node.transitions[item.NextSymbol.Name][0].idx))
                    else:
                        self._register(self.goto, (idx, item.NextSymbol.Name), (node.transitions[item.NextSymbol.Name][0].idx))
        return automaton
        
    @staticmethod
    def _register(table, key, value):
        assert key not in table or table[key] == value, 'Shift-Reduce or Reduce-Reduce conflict!!!'
        table[key] = value

