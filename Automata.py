import pydot


def move(automaton, states, symbol):
    moves = set()
    for state in states:
        try:
            for t in automaton.transitions[state][symbol]:
                moves.add(t)
        except KeyError:
            continue
    return moves

def epsilon_closure(automaton, states):
    pending = [ s for s in states ] # equivalente a list(states) pero me gusta así :p
    closure = { s for s in states } # equivalente a  set(states) pero me gusta así :p
    
    while pending:
        state = pending.pop()
        try:
            t_states = automaton.transitions[state]['']
            for s in t_states:
                if not s in closure:
                    closure.add(s)
                    pending.append(s)
                    
        except KeyError:
            continue
                
    return ContainerSet(*closure)

def nfa_to_dfa(automaton):
    transitions = {}
    
    start = epsilon_closure(automaton, [automaton.start])
    start.id = 0
    start.is_final = any(s in automaton.finals for s in start)
    states = [ start ]
    count=1

    pending = [ start ]
    while pending:
        state = pending.pop()
        
        for symbol in automaton.vocabulary:
            s=move(automaton, state, symbol)
            if s==set():
                continue
            epsilon_clousure_ = epsilon_closure(automaton, s)
            
            visited = False
            for s in states:
                if epsilon_clousure_ == s:
                    epsilon_clousure_=s
                    visited = True
            
            if not visited:
                epsilon_clousure_.id = count
                count += 1
                epsilon_clousure_.is_final = any(s in automaton.finals for s in epsilon_clousure_)
                states.append(epsilon_clousure_)
                pending.append(epsilon_clousure_)

            try:
                transitions[state.id, symbol]
                assert False, 'Invalid DFA!!!'
            except KeyError:
                transitions[state.id, symbol] = epsilon_clousure_.id
    
    finals = [ state.id for state in states if state.is_final ]
    dfa = DFA(len(states), finals, transitions)
    return dfa


def distinguish_states(group, automaton, sets):
    equivalence_classes = {}
    alphabet = tuple(automaton.vocabulary)

    for u in group:
        transitions = automaton.transitions[u.value]
        labels = [(transitions[s][0] if s in transitions else None) for s in alphabet]
        mapped_labels = [(sets[d].representative if d in sets.nodes else None) for d in labels]
        equivalence_key = tuple(mapped_labels)

        try:
            equivalence_classes[equivalence_key].append(u.value)
        except KeyError:
            equivalence_classes[equivalence_key] = [u.value]

    return [R for R in equivalence_classes.values()]

def state_minimization(automaton):
    sets = DisjointSet(*range(automaton.states))
    sets.merge(s for s in automaton.finals)
    sets.merge(s for s in range(automaton.states) if s not in automaton.finals)

    while True:
        new_sets = DisjointSet(*range(automaton.states))
        for group in sets.groups:
            for h in distinguish_states(group, automaton, sets):
                new_sets.merge(h)

        if len(new_sets) == len(sets):
            break

        sets = new_sets

    return sets

def automata_minimization(automaton):
    sets = state_minimization(automaton)
    representatives = [s for s in sets.representatives]
    transitions = {}
    for i, state in enumerate(representatives):
        value = state.value
        for symbol, label in automaton.transitions[value].items():
            target = sets[label[0]].representative
            j = representatives.index(target)
            try:
                transitions[i, symbol]
                assert False
            except KeyError:
                transitions[i, symbol] = j

    final_states = [i for i, state in enumerate(representatives) if state.value in automaton.finals]
    start_state = representatives.index(sets[automaton.start].representative)

    return DFA(len(representatives), final_states, transitions, start_state)

def automata_union(a1, a2):
    transitions = {}
    start_state = 0
    d1 = 1
    d2 = a1.states + d1
    final = a2.states + d2

    # Transitions from a1
    for (origin, symbol), destinations in a1.map.items():
        new_destinations = {dest + d1 for dest in destinations}
        transitions[(origin + d1, symbol)] = new_destinations

    # Transitions from a2
    for (origin, symbol), destinations in a2.map.items():
        new_destinations = {dest + d2 for dest in destinations}
        transitions[(origin + d2, symbol)] = new_destinations

    # Epsilon transition from start state to a1.start and a2.start
    transitions[(start_state, '')] = [a1.start + d1, a2.start + d2]

    # Epsilon transitions from a1.finals and a2.finals to final state
    for dx, final_states in zip([d1, d2], [a1.finals, a2.finals]):
        for state in final_states:
            try:
                epsilon_transitions = transitions[state + dx, '']
            except KeyError:
                epsilon_transitions = transitions[state + dx, ''] = set()
            epsilon_transitions.add(final)

    total_states = a1.states + a2.states + 2
    final_states = {final}

    return NFA(total_states, final_states, transitions, start_state)

def automata_closure(a1):
    transitions = {}
    start_state = 0
    d1 = 1
    final = a1.states + d1

    # Transitions from a1
    for (origin, symbol), destinations in a1.map.items():
        new_destinations = {dest + d1 for dest in destinations}
        transitions[(origin + d1, symbol)] = new_destinations

    # Epsilon transition from start state to a1.start and final
    transitions[(start_state, '')] = [a1.start + d1, final]

    # Epsilon transitions from a1.finals to final and a1.start+d1
    for state in a1.finals:
        try:
            epsilon_transitions = transitions[state + d1, '']
        except KeyError:
            epsilon_transitions = transitions[state + d1, ''] = set()
        epsilon_transitions.add(final)
        epsilon_transitions.add(a1.start + d1)

    total_states = a1.states + 2
    final_states = {final}

    return NFA(total_states, final_states, transitions, start_state)

def automata_concatenation(automaton1, automaton2):
    concatenated_map = {}
    total_states = 0
    delta1 = 0
    delta2 = automaton1.states + delta1
    upper_bound = automaton2.states + delta2

    for (state1, symbol), outputs in automaton1.map.items():
        concatenated_map[state1 + delta1, symbol] = {output + delta1 for output in outputs}

    for (state2, symbol), outputs in automaton2.map.items():
        concatenated_map[state2 + delta2, symbol] = {output + delta2 for output in outputs}

    for final_state1 in automaton1.finals:
        try:
            X = concatenated_map[final_state1 + delta1, '']
        except KeyError:
            X = concatenated_map[final_state1 + delta1, ''] = set()
        X.add(automaton2.start + delta2)

    for final_state2 in automaton2.finals:
        try:
            X = concatenated_map[final_state2 + delta2, '']
        except KeyError:
            X = concatenated_map[final_state2 + delta2, ''] = set()
        X.add(upper_bound)

    total_states = automaton1.states + automaton2.states + 2
    final_states = {upper_bound}

    return NFA(total_states, final_states, concatenated_map, 0)


## Automata classes

class NFA:
    def __init__(self, states, finals, transitions, start=0):
        self.states = states
        self.start = start
        self.finals = set(finals)
        self.map = transitions
        self.vocabulary = set()
        self.transitions = { state: {} for state in range(states) }
        
        for (origin, symbol), destinations in transitions.items():
            assert hasattr(destinations, '__iter__'), 'Invalid collection of states'
            self.transitions[origin][symbol] = destinations
            self.vocabulary.add(symbol)
            
        self.vocabulary.discard('')
        
    def epsilon_transitions(self, state):
        assert state in self.transitions, 'Invalid state'
        try:
            return self.transitions[state]['']
        except KeyError:
            return ()
            
    def graph(self):
        G = pydot.Dot(rankdir='LR', margin=0.1)
        G.add_node(pydot.Node('start', shape='plaintext', label='', width=0, height=0))

        for (start, tran), destinations in self.map.items():
            tran = 'ε' if tran == '' else tran
            G.add_node(pydot.Node(start, shape='circle', style='bold' if start in self.finals else ''))
            for end in destinations:
                G.add_node(pydot.Node(end, shape='circle', style='bold' if end in self.finals else ''))
                G.add_edge(pydot.Edge(start, end, label=tran, labeldistance=2))

        G.add_edge(pydot.Edge('start', self.start, label='', style='dashed'))
        return G

    def _repr_svg_(self):
        try:
            return self.graph().create_svg().decode('utf8')
        except:
            pass

class DFA(NFA):
    
    def __init__(self, states, finals, transitions, start=0):
        assert all(isinstance(value, int) for value in transitions.values())
        assert all(len(symbol) > 0 for origin, symbol in transitions)
        
        transitions = { key: [value] for key, value in transitions.items() }
        NFA.__init__(self, states, finals, transitions, start)
        self.current = start
        
    def _move(self, symbol):
        try:
            self.current = self.transitions[self.current][symbol][0]
            return True
        except KeyError:
            return False
    
    def _reset(self):
        self.current = self.start
        
    def recognize(self, string):
        i = 0
        while i < len(string) and self._move(string[i]):
            i += 1
        
        if i == len(string) and self.current in self.finals:
            self._reset()
            return True
        self._reset()
        return False
    

class Token:
    """
    Basic token class.

    Parameters
    ----------
    lex : str
        Token's lexeme.
    token_type : Enum
        Token's type.
    """

    def __init__(self, lex, token_type):
        self.lex = lex
        self.token_type = token_type

    def __str__(self):
        return f'{self.token_type}: {self.lex}'

    def __repr__(self):
        return str(self)

    @property
    def is_valid(self):
        return True
    
class State:

    def __init__(self, state, final=False, formatter=lambda x: str(x), shape='circle'):
        self.state = state
        self.final = final
        self.transitions = {}
        self.epsilon_transitions = set()
        self.tag = None
        self.formatter = formatter
        self.shape = shape

    # The method name is set this way from compatibility issues.
    def set_formatter(self, value, attr='formatter', visited=None):
        if visited is None:
            visited = set()
        elif self in visited:
            return

        visited.add(self)
        self.__setattr__(attr, value)
        for destinations in self.transitions.values():
            for node in destinations:
                node.set_formatter(value, attr, visited)
        for node in self.epsilon_transitions:
            node.set_formatter(value, attr, visited)
        return self

    def has_transition(self, symbol):
        return symbol in self.transitions

    def add_transition(self, symbol, state):
        try:
            self.transitions[symbol].append(state)
        except:
            self.transitions[symbol] = [state]
        return self

    def add_epsilon_transition(self, state):
        self.epsilon_transitions.add(state)
        return self

    def recognize(self, string):
        states = self.epsilon_closure
        for symbol in string:
            states = self.move_by_state(symbol, *states)
            states = self.epsilon_closure_by_state(*states)
        return any(s.final for s in states)

    def to_deterministic(self, formatter=lambda x: str(x)):
        closure = self.epsilon_closure
        start = State(tuple(closure), any(s.final for s in closure), formatter)

        closures = [ closure ]
        states = [ start ]
        pending = [ start ]

        while pending:
            state = pending.pop()
            symbols = { symbol for s in state.state for symbol in s.transitions }

            for symbol in symbols:
                move = self.move_by_state(symbol, *state.state)
                closure = self.epsilon_closure_by_state(*move)

                if closure not in closures:
                    new_state = State(tuple(closure), any(s.final for s in closure), formatter)
                    closures.append(closure)
                    states.append(new_state)
                    pending.append(new_state)
                else:
                    index = closures.index(closure)
                    new_state = states[index]

                state.add_transition(symbol, new_state)

        return start

    @staticmethod
    def from_nfa(nfa, get_states=False):
        states = []
        for n in range(nfa.states):
            state = State(n, n in nfa.finals)
            states.append(state)

        for (origin, symbol), destinations in nfa.map.items():
            origin = states[origin]
            origin[symbol] = [ states[d] for d in destinations ]

        if get_states:
            return states[nfa.start], states
        return states[nfa.start]

    @staticmethod
    def move_by_state(symbol, *states):
        return { s for state in states if state.has_transition(symbol) for s in state[symbol]}

    @staticmethod
    def epsilon_closure_by_state(*states):
        closure = { state for state in states }

        l = 0
        while l != len(closure):
            l = len(closure)
            tmp = [s for s in closure]
            for s in tmp:
                for epsilon_state in s.epsilon_transitions:
                        closure.add(epsilon_state)
        return closure

    @property
    def epsilon_closure(self):
        return self.epsilon_closure_by_state(self)

    @property
    def name(self):
        return self.formatter(self.state)

    def get(self, symbol):
        target = self.transitions[symbol]
        assert len(target) == 1
        return target[0]

    def __getitem__(self, symbol):
        if symbol == '':
            return self.epsilon_transitions
        try:
            return self.transitions[symbol]
        except KeyError:
            return None

    def __setitem__(self, symbol, value):
        if symbol == '':
            self.epsilon_transitions = value
        else:
            self.transitions[symbol] = value

    def __repr__(self):
        return str(self)

    def __str__(self):
        return str(self.state)

    def __hash__(self):
        return hash(self.state)

    def __iter__(self):
        yield from self._visit()

    def _visit(self, visited=None):
        if visited is None:
            visited = set()
        elif self in visited:
            return

        visited.add(self)
        yield self

        for destinations in self.transitions.values():
            for node in destinations:
                yield from node._visit(visited)
        for node in self.epsilon_transitions:
            yield from node._visit(visited)

    def graph(self):
        G = pydot.Dot(rankdir='LR', margin=0.1)
        G.add_node(pydot.Node('start', shape='plaintext', label='', width=0, height=0))

        visited = set()
        def visit(start):
            ids = id(start)
            if ids not in visited:
                visited.add(ids)
                G.add_node(pydot.Node(ids, label=start.name, shape=self.shape, style='bold' if start.final else ''))
                for tran, destinations in start.transitions.items():
                    for end in destinations:
                        visit(end)
                        G.add_edge(pydot.Edge(ids, id(end), label=tran, labeldistance=2))
                for end in start.epsilon_transitions:
                    visit(end)
                    G.add_edge(pydot.Edge(ids, id(end), label='ε', labeldistance=2))

        visit(self)
        G.add_edge(pydot.Edge('start', id(self), label='', style='dashed'))

        return G

    def _repr_svg_(self):
        try:
            return self.graph().create_svg().decode('utf8')
        except:
            pass

    def write_to(self, fname):
        return self.graph().write_svg(fname)
    
class ContainerSet:
    def __init__(self, *values, contains_epsilon=False):
        self.set = set(values)
        self.contains_epsilon = contains_epsilon

    def add(self, value):
        n = len(self.set)
        self.set.add(value)
        return n != len(self.set)

    def extend(self, values):
        change = False
        for value in values:
            change |= self.add(value)
        return change

    def set_epsilon(self, value=True):
        last = self.contains_epsilon
        self.contains_epsilon = value
        return last != self.contains_epsilon

    def update(self, other):
        n = len(self.set)
        self.set.update(other.set)
        return n != len(self.set)

    def epsilon_update(self, other):
        return self.set_epsilon(self.contains_epsilon | other.contains_epsilon)

    def hard_update(self, other):
        return self.update(other) | self.epsilon_update(other)

    def find_match(self, match):
        for item in self.set:
            if item == match:
                return item
        return None

    def __len__(self):
        return len(self.set) + int(self.contains_epsilon)

    def __str__(self):
        return '%s-%s' % (str(self.set), self.contains_epsilon)

    def __repr__(self):
        return str(self)

    def __iter__(self):
        return iter(self.set)

    def __nonzero__(self):
        return len(self) > 0

    def __eq__(self, other):
        if isinstance(other, set):
            return self.set == other
        return isinstance(other, ContainerSet) and self.set == other.set and self.contains_epsilon == other.contains_epsilon

class DisjointSet:
    def __init__(self, *items):
        self.nodes = { x: DisjointNode(x) for x in items }

    def merge(self, items):
        items = (self.nodes[x] for x in items)
        try:
            head, *others = items
            for other in others:
                head.merge(other)
        except ValueError:
            pass

    @property
    def representatives(self):
        return { n.representative for n in self.nodes.values() }

    @property
    def groups(self):
        return [[n for n in self.nodes.values() if n.representative == r] for r in self.representatives]

    def __len__(self):
        return len(self.representatives)

    def __getitem__(self, item):
        return self.nodes[item]

    def __str__(self):
        return str(self.groups)

    def __repr__(self):
        return str(self)

class DisjointNode:
    def __init__(self, value):
        self.value = value
        self.parent = self

    @property
    def representative(self):
        if self.parent != self:
            self.parent = self.parent.representative
        return self.parent

    def merge(self, other):
        other.representative.parent = self.representative

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return str(self)
