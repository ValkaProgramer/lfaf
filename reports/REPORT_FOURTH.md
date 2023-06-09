# Chomsky Normal Form

### Course: Formal Languages & Finite Automata

### Author: Luchianov Vladimir

---

## Theory

Chomsky Normal Form (CNF) is a specific form that a context-free grammar (CFG) can be transformed into, which simplifies many computational tasks on the grammar. CNF has the following two properties:

1. All productions are of the form A -> BC or A -> a, where A, B, and C are non-terminals and a is a terminal symbol.
2. The start symbol S does not appear on the right-hand side of any production.

To convert a CFG into CNF, the following steps are typically followed:

1. Remove all productions that generate the empty string (epsilon), unless the start symbol S itself generates epsilon.
2. Remove all unit productions, which are productions of the form A -> B, where A and B are non-terminals.
3. Replace all non-terminal symbols that appear in the right-hand side of productions with two non-terminal symbols, such that each production has at most two non-terminal symbols on its right-hand side.
4. Replace all productions of the form A -> a with A -> A' and A' -> a, where A' is a new non-terminal symbol.
5. Finally, introduce a new start symbol S' and a new production S' -> S, where S is the original start symbol of the grammar.

After applying these steps, the resulting grammar will be in CNF. CNF conversion is important in theoretical computer science and natural language processing because it simplifies the analysis of CFGs and enables the use of efficient parsing algorithms.

## Objectives:

1. Learn about Chomsky Normal Form (CNF) [1].
2. Get familiar with the approaches of normalizing a grammar.
3. Implement a method for normalizing an input grammar by the rules of CNF.
   1. The implementation needs to be encapsulated in a method with an appropriate signature (also ideally in an appropriate class/type).
   2. The implemented functionality needs executed and tested.
   3. A BONUS point will be given for the student who will have unit tests that validate the functionality of the project.
   4. Also, another BONUS point would be given if the student will make the aforementioned function to accept any grammar, not only the one from the student's variant.

## Implementation description

In this lab I added a method called _toCNF_ to **Grammar** which converts an object which called it and returns a tuple of arguments which can be used to create a new **Grammar** object equivalent to the initial one by grammar rules according Chomsky Normal form. The method works with any CFG.

```
    def toCNF(self):

```

I created variables to store new production dictionary, sets of new terminal and terminal symbols. Also I declared a list and a dictionary in order to compute these assets.

```

        epsilon = []
        newP = {}
        newVT = set()
        newVN = set()
        temp = {}
```
In this piece of code the method determines if new state should take place.
```
        new_state = False

        for N, productions in self.P.items():
            for production in productions:
                if 'S' in production:
                    new_state = True

```
Here the new start state is created if there is a need
```
        if new_state:
            new_start = 'Z'
            temp['Z'] = ['S']
```
In this piece of code a set of non-terminal symbols with e-productions is computed 
```
        for N, productions in self.P.items():
            for production in productions:
                if not production:
                    epsilon.append(N)
```
In this piece of code a copy of the initial production is created
```
        for key in self.P.keys():
            temp[key] = self.P[key].copy()
```
Furthermore, in a while loop for every stored nt symbol the procedure of eliminating epsilon-production initiates.
```
        while(epsilon):
            for state in epsilon:
                for NT in self.P.keys():
                    additional = []
                    for production in self.P[NT]:
                        if(state in production):
                            amount = production.count(state)
                            indices = []
                            for index in range(len(production)):
                                if production[index] == state:
                                    indices.append(index)
                            for integer in range(pow(2, amount)):
                                bin = str(format(integer, 'b'))
                                to_add = production
                                index = amount - 1
                                for item in reversed(bin):
                                    if item == '1':
                                        to_add = to_add[:indices[index]] + to_add[indices[index] + 1:]
                                    index -= 1
                                additional.append(to_add)
                    for item in additional:
                        if item not in temp[NT]:
                            temp[NT].append(item)
```
Current nt symbol's with epsilon-production removal from the queue comes next
```
                for N, productions in temp.items():
                    for index in range(len(productions)):
                        if not productions[index] and N == state:
                            productions.pop(index)
                            epsilon.remove(state)
                            break
```
Checking for new such symbols comes right after
```
            for N, productions in temp.items():
                for production in productions:
                    if not production and N not in epsilon:
                        epsilon.append(N)
```
Unit productions removal comes next. While loop continues until no unit productions are found in the temporary storage of the new production. It also contains a loop inside which deletes unit production and adds each deleted right side non-terminal symbol productions to the productions of the left side non-terminal symbol
```
        some_bool = False

        for N in temp.keys():
            additional = []
            for production in temp[N]:
                for state in temp.keys():
                    if production == state:
                        some_bool = True

        while(some_bool):
            for N in temp.keys():
                additional = []
                for production in temp[N]:
                    for state in temp.keys():
                        if production == state:
                            additional += temp[state]
                            temp[N].remove(state)
                for item in additional:
                    if item not in temp[N]:
                        temp[N].append(item)

            some_bool = False

            for N in temp.keys():
                    additional = []
                    for production in temp[N]:
                        for state in temp.keys():
                            if production == state:
                                some_bool = True
```
Next piece of code performs a search of productions containing both non-terminal and terminal symbols on the right side.
```
        additional_VT = {}
        for N, productions in temp.items():
            for production in productions:
                for symbol in production:
                    if symbol in self.VT and not production == symbol and symbol not in additional_VT:
                        additional_VT[symbol] = []

        for key in additional_VT.keys():
            for N in temp.keys():
                if len(temp[N]) == 1 and temp[N][0] == symbol and N not in additional_VT[symbol]:
                    additional_VT[symbol].append(N)
```
Making a different A -> a type production for each terminal symbol found and adding these productions to the temporal storage of the new production.
```
        for key in additional_VT.keys():
            if not additional_VT[key]:
                for index in range(len(string.ascii_uppercase)):
                    if string.ascii_uppercase[index] not in temp.keys():
                        additional_VT[key] = [string.ascii_uppercase[index]]
                        break

        for key in additional_VT.keys():
            if additional_VT[key][0] not in temp.keys():
                temp[additional_VT[key][0]] = [key]
```
Replacing every terminal symbol in productions found previously with new non-terminal symbols
```
        for symbol in additional_VT.keys():
            for N in temp.keys():
                for number in range(len(temp[N])):
                    if not temp[N][number] == symbol:
                        result = ''
                        for index in range(len(temp[N][number])):
                            if temp[N][number][index] == symbol:
                                result += additional_VT[symbol][0]
                            else:
                                result += temp[N][number][index]
                        temp[N][number] = result
```
Next comes the process of eliminating A -> A1..An productions. Initially creates an empty tuple for storing productions to be changed and a while loop helper variable assigned to True.
```
        binFound = True
        toReplace = ()
```
Right after a while loop is perfomed, which runs until no such productions are found. This loop contains another loop which runs through every production and creates new production Xi -> Ai-1Ai
```
        while binFound:
            binFound = False
            for N in temp.keys():
                for production in temp[N]:
                    if len(production) > 2:
                        binFound = True
                        for index in range(len(string.ascii_uppercase)):
                            if string.ascii_uppercase[index] not in temp.keys():
                                temp[string.ascii_uppercase[index]] = [production[:2]]
                                toReplace = (string.ascii_uppercase[index], production[:2])
                                break
                    if binFound:
                        break
                if binFound:
                    break
            if toReplace:
                for N in temp.keys():
                    for index in range(len(temp[N])):
                        if toReplace[1] in temp[N][index] and len(temp[N][index]) > 2:
                            temp[N][index] = temp[N][index].replace(toReplace[1], toReplace[0])
```
Next step the method perfoms is deleting unaccesable symbols. Firstly it detects non-terminal symbols to be deleted.
```
        toDelete = []

        for state in temp.keys():
            notUsed = True
            for N, productions in temp.items():
                for production in productions:
                    for symbol in production:
                        if symbol == state or state in new_start:
                            notUsed = False
                            break
                    if not notUsed:
                        break
                if not notUsed:
                    break
            if notUsed:
                toDelete.append(state)
```
Then the method deletes them in a single for loop
```
        for item in toDelete:
            temp.pop(item)
```
Assigning values of temporal variables to the final ones
```
        for key in temp.keys():
            newVN.add(key)
            for production in temp[key]:
                for symbol in production:
                    if symbol in string.ascii_lowercase:
                        newVT.add(symbol)

        newP = temp.copy()
```
Returning a tuple of arguments convenient for making a CNF **Grammar** object, equivalent to the initial by grammar rules
```
        return (newVN, newVT, newP, new_start)
```

Drive code to test the functionality of the implemented method:

```
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
```

## Conclusions / Screenshots / Results

In this laboratory work I implemented the conversion of any Context-Free Grammar to a Chomsky Normal form Grammar. I learned a lot about Chomsky Normal form. I learned how to procceed in a way to convert it in general and how to solve problems appearing during implementation.
