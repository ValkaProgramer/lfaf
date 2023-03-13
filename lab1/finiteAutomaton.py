class FiniteAutomaton:
    def __init__(self, grammar):
        self.states = grammar.VN
        self.inputs = grammar.VT
        self.final_states = self.getFinalStates(grammar.P)
        self.transitions = self.getTransitions(grammar.P)

    def getFinalStates(self, P):
        final = []

        for state in self.states:
            for input in P[state]:
                if input in self.inputs:
                    final.append(state)
                    break

        return final

    def getTransitions(self, P):
        transitions = {}

        for state in self.states:
            for transition in P[state]:
                next_char = None
                next_state = None

                for char in transition:
                    if char in self.states:
                        next_state = char
                    else:
                        next_char = char

                transitions[(state, next_char)] = next_state if next_state else state

        return transitions
    
    def stringBelongsToLanguage(self, string):
        current_state = "S"

        for char in string:
            if (current_state, char) not in self.transitions:
                return False
            
            current_state = self.transitions[(current_state, char)]

        return current_state in self.final_states
