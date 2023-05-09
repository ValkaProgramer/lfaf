import random
import string

class Grammar:
    def __init__(self, argTuple):
        VN, VT, P, start = argTuple
        self.VN = VN
        self.VT = VT
        self.P = P
        self.start = start

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
        dictionary = {self.start : 'q0'}

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
    
    def toCNF(self):

        epsilon = []
        newP = {}
        newVT = set()
        newVN = set()
        temp = {}

        new_state = False

        for N, productions in self.P.items():
            for production in productions:
                if 'S' in production:
                    new_state = True

        if new_state:
            new_start = 'Z'
            temp['Z'] = ['S']

        for N, productions in self.P.items():
            for production in productions:
                if not production:
                    epsilon.append(N)

        for key in self.P.keys():
            temp[key] = self.P[key].copy()

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

                for N, productions in temp.items():
                    for index in range(len(productions)):
                        if not productions[index] and N == state:
                            productions.pop(index)
                            epsilon.remove(state)
                            break

            for N, productions in temp.items():
                for production in productions:
                    if not production and N not in epsilon:
                        epsilon.append(N)

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
        
        for key in additional_VT.keys():
            if not additional_VT[key]:
                for index in range(len(string.ascii_uppercase)):
                    if string.ascii_uppercase[index] not in temp.keys():
                        additional_VT[key] = [string.ascii_uppercase[index]]
                        break


        for key in additional_VT.keys():
            if additional_VT[key][0] not in temp.keys():
                temp[additional_VT[key][0]] = [key]


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

        binFound = True
        toReplace = ()

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
            
        for item in toDelete:
            temp.pop(item)

        for key in temp.keys():
            newVN.add(key)
            for production in temp[key]:
                for symbol in production:
                    if symbol in string.ascii_lowercase:
                        newVT.add(symbol)

        newP = temp.copy()

        return (newVN, newVT, newP, new_start)