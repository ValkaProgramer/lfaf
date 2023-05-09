# Determinism in Finite Automata. Conversion from NDFA 2 DFA. Chomsky Hierarchy.

### Course: Formal Languages & Finite Automata

### Author: Luchianov Vladimir

---

## Theory

A finite automaton is a mechanism used to model different processes, and its structure is similar to that of a state machine. The term "finite" refers to the fact that an automaton has a starting state and a set of final states, which means that each process modeled by an automaton has a clear beginning and end.

However, there are situations where a single transition can lead to multiple states, which creates a problem known as non-determinism. In the field of systems theory, the degree of determinism in a system is used to measure its predictability. If a system involves random variables, it becomes stochastic or non-deterministic.

Finite automata can be classified as either deterministic or non-deterministic, depending on their structure. It is possible to achieve determinism by following certain algorithms that modify the structure of the automaton. These algorithms can be used to eliminate non-deterministic behavior and improve the predictability of the system.

## Objectives:

1. Understand what an automaton is and what it can be used for.

2. Continuing the work in the same repository and the same project, the following need to be added:
   a. Provide a function in your grammar type/class that could classify the grammar based on Chomsky hierarchy.

   b. For this you can use the variant from the previous lab.

3. According to your variant number (by universal convention it is register ID), get the finite automaton definition and do the following tasks:

   a. Implement conversion of a finite automaton to a regular grammar.

   b. Determine whether your FA is deterministic or non-deterministic.

   c. Implement some functionality that would convert an NDFA to a DFA.

   d. Represent the finite automaton graphically (Optional, and can be considered as a **_bonus point_**):

   - You can use external libraries, tools or APIs to generate the figures/diagrams.
   - Your program needs to gather and send the data about the automaton and the lib/tool/API return the visual representation.

## Implementation description

In this lab I changed the structure of the project a bit. **FiniteAutomaton** and **Grammar** classes now have constructors accepting a tuple of values and assign these values to their object's attributes.

```
def __init__(self, argTuple):
        VN, VT, P = argTuple
        self.VN = VN
        self.VT = VT
        self.P = P

def __init__(self, argTuple):
        states, inputs, final, transitions = argTuple
        self.states = states
        self.inputs = inputs
        self.final_states = final
        self.transitions = transitions
```

**Grammar** class now have a method called _chomskyType_ which returns a string containing information about the **Grammar** object called it

```
    def chomskyType(self):
        if all(len(lhs) == 1 and lhs in self.VN for lhs in self.P.keys()) and all(len(rhs) <= 2 and (rhs[0] in self.VT or rhs[0] == '') and (len(rhs) == 1 or (len(rhs) == 2 and rhs[1] in self.VN)) for rhs_list in self.P.values() for rhs in rhs_list):
            return "Type 3 (regular)"

        if all(len(lhs) == 1 and lhs in self.VN for lhs in self.P.keys()) and all(p in self.VN + self.VT for rhs_list in self.P.values() for rhs in rhs_list for p in rhs):
            return "Type 2 (context-free)"

        if all(len(lhs) <= len(rhs) for lhs, rhs_list in self.P.items() for rhs in rhs_list) and "S" in self.VN and all(p in self.VN + self.VT for rhs_list in self.P.values() for rhs in rhs_list for p in rhs):
            return "Type 1 (context-sensitive)"

        if not all(p.isupper() or p == '' for rhs in self.P.values() for p in rhs):
            return "Type 0 (unrestricted)"

        return "Not a valid Chomsky hierarchy type"
```

**FiniteAutomaton** class now have a method called _faToRg_ which converts own attributes according some rules and returns a tuple of arguments which can be used as a parameter of construncting new **Grammar** object equivalent to **FiniteAutomaton** object.

```
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
```

Also it has a method to convert obejct called it and returns a new DFA **FiniteAutomaton** object equivalent to the first one by Automata rules

```
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
```

As a bonus point I tried to implement graphical representation of automatons, using visual_automata library, but failed

```
from visual_automata.fa.nfa import VisualNFA
from visual_automata.fa.dfa import VisualDFA
from automata.fa.dfa import DFA

visual_transitions = {}

for state in dfa.states:
    visual_transitions[state] = {}
    for input in dfa.inputs:
        if(dfa.transitions[state][input]):
            visual_transitions[state][input] = set([dfa.transitions[state][input]])
print(visual_transitions)

visual = VisualDFA(
    states = dfa.states,
    input_symbols = dfa.inputs,
    transitions = dfa.transitions,
    initial_state = "q0",
    final_states = dfa.final_states
)

visual.show_diagram(view=True)
```

## Conclusions / Screenshots / Results

In this laboratory work I implemented certain functionality of **Grammar** and **FiniteAutomaton** classes. I learned how can they be transformed each into other. I learned to convert a NFA to a DFA, to convert a FA to RG and to check grammar's Chomsky Hierarchy type.
