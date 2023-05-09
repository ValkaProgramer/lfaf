from grammar import Grammar
from finiteAutomaton import FiniteAutomaton
from visual_automata.fa.nfa import VisualNFA
grTuple = (
    {'S', 'A', 'B', 'C', 'D'},
    {'a', 'b'},
    {
        'S' : ['BaB', 'A'],
        'A' : ['bAa', 'aS', 'a'],
        'B' : ['AbB', 'BS', 'a', ''],
        'C' : ['BA'],
        'D' : ['a']
    },
    {'S'}
)

rg = Grammar(grTuple)

cnf = Grammar(rg.toCNF())

print(cnf.VN)
print(cnf.VT)
print(cnf.P)
print(cnf.start)