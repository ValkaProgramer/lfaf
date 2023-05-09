import random

class Grammar:
    def __init__(self, VN, VT, P):
        self.VN = VN
        self.VT = VT
        self.P = P

    def generateWord(self, non_terminal = "S"):
        word = ""
        transition = random.choice(self.P[non_terminal])

        for char in transition:
            word += self.generateWord(char) if char in self.VN else char

        return word