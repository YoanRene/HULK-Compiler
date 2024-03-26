from Automata import *
from Regex import *

class Lexer:
    def __init__(self, table, eof):
        self.eof = eof
        self.regexs = self._build_regexs(table)
        self.automaton = self._build_automaton()
    
    def _build_regexs(self, table):
        '''This function will return a list of automata that recognize the tokens of the language'''
        regexs = []
        for n, (token_type, regex) in enumerate(table):
            regex_instance = Regex(regex) #converting to a regex instance
            automaton = regex_instance.automaton # Getting the automaton from the regex
            start_state,states=State.from_nfa(automaton,get_states=True) # Getting the start state of the automaton
            for state in automaton.finals: # Tagging the final states with token_type and priority
                final_state=states[state]
                final_state.tag=(
                    n,
                    token_type
                )
            regexs.append(start_state)
            
        return regexs
    
    def _build_automaton(self):
        '''This function will return the automaton that recognizes the tokens of the language'''
        start = State('start')
        for automaton in self.regexs:
            start.add_epsilon_transition(automaton)
        return start.to_deterministic()
    
        
    def _walk(self, string):
        '''This function will return the final state and the lexeme of the string'''
        state = self.automaton
        final = state if state.final else None
        final_lex = lex = ''

        for symbol in string:

            if state:
        
                if symbol in state.transitions:
                    state = state.transitions[symbol][0]
                    lex += symbol
                    if state.final:
                        final = state
                        final_lex = lex
                else:
                    break
            else:
                break
            
        return final, final_lex
    
    def _tokenize(self, text):
        '''This function will return the tokens of the text'''
        while text:
            final, lex = self._walk(text)
            if final is None:
                yield '$',self.eof
                return
            
            priority = float('inf')
            for s in final.state:
                if s.final:
                    (p,ttype) = s.tag
                    if p< priority:
                        priority = p
                        token_type = ttype
            yield lex,token_type
            text=text[len(lex):]
        
        yield '$', self.eof
    
    def __call__(self, text):
        return [ Token(lex, ttype) for lex, ttype in self._tokenize(text) ]