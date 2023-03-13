##Vladimir Luchianov FAF-212 Lab 1

Variant 14:

VN={S, B, D},

VT={a, b, c, d},

P={

S → aS

S → bB

B → cB

B → d

B → aD

D → aB

D → b

}

I created two classes named **Grammar** and **FiniteAutomaton**.
**Grammar** class has a constructor assigning object's attributes(VN, VT and P) to given values at the initialization and a method, called *generateWord*, which generates a word picking random transitions.

**FiniteAutomaton** class also has a constructor assigning its attributes according to given grammar object. Two attributes are assigned to a computed value by its two methods, according to **Grammar** object's P value. These two methods, called *getFinalStates* and *getTransitions*, obtain values for corresponding attributes based on research of given **Grammar** object. The third method, called *stringBelongsToLanguage*, receives any string and checks if it corresponds to given grammar step-by-state.

**Main** file takes given data and makes **Grammar** object of it, makes **FiniteAutomaton** object of **Grammar** object and runs *generateWord* method five times, printing returned string alongside with an approval or disproval of belonging this string to given language, basing on returned value of *stringBelongsToLanguage* method, called with this string as an argument.