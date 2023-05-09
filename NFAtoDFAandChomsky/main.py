from grammar import Grammar
from finiteAutomaton import FiniteAutomaton
from visual_automata.fa.nfa import VisualNFA
from visual_automata.fa.dfa import VisualDFA
from automata.fa.dfa import DFA

# Variant 14
# Q = {q0,q1,q2},
# ∑ = {a,b,c},
# F = {q2},
# δ(q0,a) = q0,
# δ(q0,b) = q1,
# δ(q1,c) = q1,
# δ(q1,c) = q2,
# δ(q2,a) = q0,
# δ(q1,a) = q1.

tupleFA = ({'q0', 'q1', 'q2'}, {'a', 'b', 'c'}, {'q2'},
    {
        'q0': {
            'a' : {'q0'},
            'b' : {'q1'},
            'c' : {},
        },
        'q1' : {
            'a' : {'q1'},
            'b' : {},
            'c' : {'q1', 'q2'},
        },
        'q2' : {
            'a' : {'q0'},
            'b' : {},
            'c' : {},
        }
    })

test = FiniteAutomaton(tupleFA)

dfa = test.ndfaToDfa()

# print(test.states)
# print(test.inputs)
# print(test.final_states)
# print(test.transitions)

# print(dfa.states)
# print(dfa.inputs)
# print(dfa.final_states)
# print(dfa.transitions)

rg = Grammar(dfa.faToRg())

print(rg.VN)
print(rg.VT)
print(rg.P)

fa = FiniteAutomaton(rg.rgToFa())

print(fa.inputs)
print(fa.states)
print(fa.final_states)
print(fa.transitions)


# visual_transitions = {}

# for state in dfa.states:
#     visual_transitions[state] = {}
#     for input in dfa.inputs:
#         if(dfa.transitions[state][input]):
#             visual_transitions[state][input] = set([dfa.transitions[state][input]])
# print(visual_transitions)

# visual = VisualDFA(
#     states = dfa.states,
#     input_symbols = dfa.inputs,
#     transitions = dfa.transitions,
#     initial_state = "q0",
#     final_states = dfa.final_states
# )

# visual.show_diagram(view=True)