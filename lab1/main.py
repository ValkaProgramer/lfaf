from grammar import Grammar
from finiteAutomaton import FiniteAutomaton

VN = ["S", "B", "D"]
VT = ["a", "b", "c", "d"]
P = {
    "S":["aS", "bB"],
    "B":["cB", "d", "aD"],
    "D":["aB", "b"]
}

grammar = Grammar(VN, VT, P)
auto = FiniteAutomaton(grammar)

for _ in range(5):
    string = grammar.generateWord()
    print(f"""{string} - {"Belongs" if auto.stringBelongsToLanguage(string) else "Doesn't belong"}""")