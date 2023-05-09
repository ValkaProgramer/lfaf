import string

class FiniteAutomaton:
    def __init__(self, argTuple):
        states, inputs, final, transitions = argTuple
        self.states = states
        self.inputs = inputs
        self.final_states = final
        self.transitions = transitions
    
    def stringBelongsToLanguage(self, string):
        current_state = "q0"

        for char in string:
            if (current_state, char) not in self.transitions:
                return False
            
            current_state = self.transitions[(current_state, char)]

        return current_state in self.final_states
    
    def faToRg(self):
        # Define empty set of rules
        rules = {}
        counter = 0
        dictionary = {'q0' : 'S'}


        for state in self.states:
            if(state != 'q0'):
                dictionary[state] = string.ascii_uppercase[counter]
                counter += 1
                
        # Generate rules for each transition in Delta
        # for (q, a), next_state in self.transitions.items():
        for state in self.states:
            for input in self.inputs:
                next = self.transitions[state][input]
                if dictionary[state] not in rules:
                    rules[dictionary[state]] = []
                if(next):
                    rules[dictionary[state]].append(input + (dictionary[next] if dictionary[next] else ''))
            
        # Generate the set of non-terminal symbols
        non_terminal_symbols = list(rules.keys())

        # Generate the dictionary of production rules
        productions = {}
        for non_terminal in non_terminal_symbols:
            productions[non_terminal] = []
            for production in rules[non_terminal]:
                productions[non_terminal].append(production)
                
            if(non_terminal in [dictionary[item] for item in self.final_states]):
                productions[non_terminal].append('')
        
        
        # Return the regular grammar
        return (non_terminal_symbols, self.inputs, productions)

    def ndfaToDfa(self):

        temp_bool = True
        for state in self.states:
            for input in self.inputs:
                if(len(self.transitions[state][input]) > 1):
                    temp_bool = False
        if(temp_bool):
            return self

        new_states = set()
        new_final_states = set()
        new_transistions = {}

        new_states.add('q0')

        queue = ['q0']

        while queue:
            current_state = queue.pop(0)
            new_transistions[current_state] = {}

            some = {current_state[i : i + 2] for i in range(0, len(current_state), 2)}
            for some_final in some:
                if(some_final in self.final_states):
                    new_final_states.add(current_state)

            for input in self.inputs:
                temp = ''
                for state in some:
                    for item in self.transitions[state][input]:
                        temp += item
                result = [symbol for symbol in temp if symbol.isdigit()]
                result.sort()
                final = ''
                for item in result:
                    final += 'q' + item

                new_transistions[current_state][input] = final

            next_states = set()
            for input in self.inputs:
                if new_transistions[current_state][input]:
                    temp = ''
                    for item in new_transistions[current_state][input]:
                        temp += item
                    next_states.add(temp)
            
            for state in next_states:
                if(state not in new_states):
                    queue.append(state)
                    new_states.add(state)

        return FiniteAutomaton((new_states, self.inputs, new_final_states, new_transistions))