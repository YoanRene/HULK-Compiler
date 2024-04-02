from Parser import Item,State,compute_firsts,compute_follows
from ParserLR1 import ShiftReduceParser

def build_LR0_automaton(G):
    assert len(G.startSymbol.productions) == 1, 'Grammar must be augmented'

    start_production = G.startSymbol.productions[0]
    start_item = Item(start_production, 0)

    automaton = State(start_item, True)

    pending = [ start_item ]
    visited = { start_item: automaton }

    while pending:
        current_item = pending.pop()
        if current_item.IsReduceItem:
            continue
        
        state = visited[current_item]
        next_item = current_item.NextItem()
        try:
            new_state = visited[next_item]
        except KeyError:
            visited[next_item] = State(next_item, True)
            new_state = visited[next_item]
            pending.append(next_item)
        
        next_symbol = current_item.NextSymbol
        state.add_transition(next_symbol.Name, new_state)
        
        if next_symbol.IsNonTerminal:
            for prod in next_symbol.productions:
                item = Item(prod, 0)
                try:
                    visited[item]
                except KeyError:
                    visited[item] = State(item, True)
                    pending.append(item)
                state.add_epsilon_transition(visited[item])

        current_state = visited[current_item]
    return automaton

class SLR1Parser(ShiftReduceParser):

    def _build_parsing_table(self):
        G = self.G.AugmentedGrammar(True)


        firsts = compute_firsts(G)
        follows = compute_follows(G, firsts)
        
        automaton = build_LR0_automaton(G).to_deterministic()
        for i, node in enumerate(automaton):
            if self.verbose: print(i, '\t', '\n\t '.join(str(x) for x in node.state), '\n')
            node.idx = i

        prodOk = G.startSymbol.productions[0]

        for node in automaton:
            idx = node.idx
            for state in node.state:
                item = state.state
                # Your code here!!!
                if item.IsReduceItem:
                    if item.production == prodOk:
                        self._register(self.action, (idx, self.G.EOF.Name),(self.OK, 1))
                        continue
                    
                    for follow in follows[item.production.Left]:
                        self._register(self.action, (idx, follow.Name), (self.REDUCE, item.production))
                        
                else:
                    if item.NextSymbol.IsTerminal:
                        self._register(self.action, (idx, item.NextSymbol.Name), (self.SHIFT, node.transitions[item.NextSymbol.Name][0].idx))
                    else:
                        self._register(self.goto, (idx, item.NextSymbol.Name), (node.transitions[item.NextSymbol.Name][0].idx))
        

                # - Fill `self.Action` and `self.Goto` according to `item`)
                # - Feel free to use `self._register(...)`)
        return automaton
    
    @staticmethod
    def _register(table, key, value):
        assert key not in table or table[key] == value, 'Shift-Reduce or Reduce-Reduce conflict!!!'
        table[key] = value