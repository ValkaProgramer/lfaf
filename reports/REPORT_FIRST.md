# Intro to formal languages. Regular grammars. Finite Automata.

### Course: Formal Languages & Finite Automata

### Author: Luchianov Vladimir

---

## Theory

A finite automaton is a mechanism used to model different processes, and its structure is similar to that of a state machine. The term "finite" refers to the fact that an automaton has a starting state and a set of final states, which means that each process modeled by an automaton has a clear beginning and end.

However, there are situations where a single transition can lead to multiple states, which creates a problem known as non-determinism. In the field of systems theory, the degree of determinism in a system is used to measure its predictability. If a system involves random variables, it becomes stochastic or non-deterministic.

Finite automata can be classified as either deterministic or non-deterministic, depending on their structure. It is possible to achieve determinism by following certain algorithms that modify the structure of the automaton. These algorithms can be used to eliminate non-deterministic behavior and improve the predictability of the system.

## Objectives:

- Understand what a language is and what it needs to have in order to be considered a formal one.
- Provide the initial setup for the evolving project that you will work on during this semester. I said project because usually at lab works, I encourage/impose students to treat all the labs like stages of development of a whole project. Basically you need to do the following:  
a. Create a local && remote repository of a VCS hosting service (let us all use Github to avoid unnecessary headaches);  
b. Choose a programming language, and my suggestion would be to choose one that supports all the main paradigms;  
c. Create a separate folder where you will be keeping the report. This semester I wish I won't see reports alongside source code files, fingers crossed;
- According to your variant number (by universal convention it is register ID), get the grammar definition and do the following tasks:  
a. Implement a type/class for your grammar;  
b. Add one function that would generate 5 valid strings from the language expressed by your given grammar;  
c. Implement some functionality that would convert and object of type Grammar to one of type Finite Automaton;  
d. For the Finite Automaton, please add a method that checks if an input string can be obtained via the state transition from it;

## Implementation description

I created two classes named **Grammar** and **FiniteAutomaton**.
**Grammar** class has a constructor assigning object's attributes(VN, VT and P) to the given values at the initialization

```
class Grammar:
    def __init__(self, VN, VT, P):
        self.VN = VN
        self.VT = VT
        self.P = P
```
and a method, called _generateWord_, which generates a word picking random transitions.
```
    def generateWord(self, non_terminal = "S"):
        word = ""
        transition = random.choice(self.P[non_terminal])

        for char in transition:
            word += self.generateWord(char) if char in self.VN else char

        return word
```

**FiniteAutomaton** class also has a constructor assigning its attributes according to given grammar object. Two attributes are assigned to a computed value by its two methods, according to **Grammar** object's P value.
```
class FiniteAutomaton:
    def __init__(self, grammar):
        self.states = grammar.VN
        self.inputs = grammar.VT
        self.final_states = self.getFinalStates(grammar.P)
        self.transitions = self.getTransitions(grammar.P)
```
These two methods, called _getFinalStates_ and _getTransitions_, obtain values for corresponding attributes based on research of the given **Grammar** object.
```
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
```
The third method, called _stringBelongsToLanguage_, receives any string and checks if it corresponds to given grammar step-by-state.
```
    def stringBelongsToLanguage(self, string):
        current_state = "S"

        for char in string:
            if (current_state, char) not in self.transitions:
                return False
            
            current_state = self.transitions[(current_state, char)]

        return current_state in self.final_states
```

**Main** file takes given data
```
from grammar import Grammar
from finiteAutomaton import FiniteAutomaton

VN = ["S", "B", "D"]
VT = ["a", "b", "c", "d"]
P = {
    "S":["aS", "bB"],
    "B":["cB", "d", "aD"],
    "D":["aB", "b"]
}
```
and makes **Grammar** object of it, makes **FiniteAutomaton** object of **Grammar** object
```
grammar = Grammar(VN, VT, P)
auto = FiniteAutomaton(grammar)
```
and runs _generateWord_ method five times, printing returned string alongside with an approval or disproval of belonging this string to given language, basing on returned value of _stringBelongsToLanguage_ method, called with this string as an argument.
```
for _ in range(5):
    string = grammar.generateWord()
    print(f"""{string} - {"Belongs" if auto.stringBelongsToLanguage(string) else "Doesn't belong"}""")
```
Here's some code results:
```
baaaacab - Belongs
aaabaad - Belongs  
bd - Belongs       
abccd - Belongs    
aaaabaaab - Belongs
```
```
bd - Belongs
aabccd - Belongs    
bccab - Belongs     
bd - Belongs        
baaccaacab - Belongs
```

## Conclusions / Screenshots / Results
In this laboratory work I implemented the concept of regular grammar and finite automaton. I learned how they work and their relationship with each other. I learned to convert a regular grammar to a finite automaton and check the corresponding strings through it.