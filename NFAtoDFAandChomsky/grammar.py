import random

class Grammar:
    def __init__(self, argTuple):
        VN, VT, P = argTuple
        self.VN = VN
        self.VT = VT
        self.P = P

    def generateWord(self, non_terminal = "S"):
        word = ""
        transition = random.choice(self.P[non_terminal])

        for char in transition:
            word += self.generateWord(char) if char in self.VN else char

        return word
    
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

    def rgToFa(self):

        # Create an empty transition function
        Delta = {}
        counter = 1
        dictionary = {'S' : 'q0'}

        for state in self.VN:
            if(state != 'S'):
                dictionary[state] = 'q' + str(counter)
                counter += 1

        # Add transitions for each production rule
        for A, productions in self.P.items():
            for production in productions:
                if len(production) == 1:
                    # Production is of the form A -> a
                    a = production
                    if dictionary[A] not in Delta:
                        Delta[dictionary[A]] = {}
                    if(a not in Delta[dictionary[A]]):
                        Delta[dictionary[A]][a] = 'E'
                    
                elif len(production) == 2:
                    # Production is of the form A -> aB
                    a, B = production
                    if dictionary[A] not in Delta:
                        Delta[dictionary[A]] = {}
                    if(a not in Delta[dictionary[A]]):
                        Delta[dictionary[A]][a] = dictionary[B]

        # Return the FA tuple (Q, Sigma, Delta, F)
        return (self.VN + ["E"], self.VT, ["E"], Delta)