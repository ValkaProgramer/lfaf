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
            tokens_space = lexeme.split()
            tokens = []
            round_met = False
            for cindex in range(len(tokens_space)):
                if tokens_space[cindex] == '"':
                    tokens.append('"')
                    round_met = not round_met
                    temp = '$'
                    for jndex in range(cindex + 1, len(tokens_space)):
                        if tokens_space[jndex] == '"':
                            for tindex in range(cindex + 1, jndex):
                                temp += tokens_space[tindex]
                    tokens.append(temp)
                elif not round_met:
                    tokens.append(tokens_space[cindex])
            total_tokens.append([])
            for token in tokens:
                for key in self.tokens.keys():
                    if token in self.tokens[key]:
                        typ = key
                        break
                    elif token[0] == '$':
                        token = token[1:]
                        typ = "string"
                        break     
                    typ = 'identifier'
                total_tokens[index].append((token, typ))

        return total_tokens