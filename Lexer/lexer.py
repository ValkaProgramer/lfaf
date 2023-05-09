class Lexer:
    
    def __init__(self, argTuple):
        tokens, splits = argTuple
        self.tokens = tokens
        self.splits = splits

    def lexing(self, string):
        total_tokens = []
        lexemes = []
        last_index = -1
        for index in range(len(string)):
            if string[index] in self.splits:
                lexemes.append(string[last_index + 1:index + 1])
                last_index = index
        
        for index in range(len(lexemes)):
            lexeme = lexemes[index]
            tokens = lexeme.split()
            total_tokens.append([])
            for token in tokens:
                for key in self.tokens.keys():
                    if token in self.tokens[key]:
                        typ = key
                        break
                    typ = 'identifier'
                total_tokens[index].append((token, typ))

        return total_tokens