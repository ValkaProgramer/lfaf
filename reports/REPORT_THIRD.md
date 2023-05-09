# Lexer & Scanner

### Course: Formal Languages & Finite Automata

### Author: Luchianov Vladimir

---

## Theory

The process of extracting lexical tokens from a string of characters is known as lexical analysis, which is commonly referred to as lexer. The term lexer is often used interchangeably with other names, such as tokenizer or scanner. Lexer is an essential component of a compiler/interpreter used in handling programming, markup or other types of languages.

The lexer applies rules of the language to identify tokens from the input stream, which are also called lexemes. Lexemes are produced by splitting the input based on delimiters, such as spaces. In contrast, tokens are assigned categories or names to each lexeme and may contain additional metadata but do not necessarily retain the actual value of the lexeme. The lexer produces a stream of tokens, which distinguishes it from lexemes.

## Objectives:

1. Understand what lexical analysis [1] is.
2. Get familiar with the inner workings of a lexer/scanner/tokenizer.
3. Implement a sample lexer and show how it works.

## Implementation description

In this lab I added **Lexer** class which contains the dictionary type _tokens_ and the list type _splits_ attributes. They are assigned as an object of this type is created by constructor.

```
class Lexer:

    def __init__(self, argTuple):
        tokens, splits = argTuple
        self.tokens = tokens
        self.splits = splits
```

Class **Lexer** contains a method called _lexing_ which accepts a string to be processed. As it iterates the given string it splits the string in lexemes first, then in tokens determining its type. The method returns a list of list type lexemes of tuples which contain tokens and their type

```
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
```

Drive code for creating a **Lexer** object and lexing a string:

```
from lexer import Lexer

lexer = Lexer(({'keywords' : ['int', 'scanf'],
                'separator' : [',', ';', '"', '(', ')'],
                'operator' : ['&', '=', '*']},
                [';']))

print(lexer.lexing('int work_interval_count , mode1 , mode2 , mode3 , afk1 , afk2 ; scanf ( " %d %d %d %d %d %d " , & work_interval_count , & mode1 , & mode2 , & mode3 , & afk1 , & afk2 ) ; works = ( int * ) ;'))
```

## Conclusions / Screenshots / Results

In this laboratory work I implemented a lexer which accepts split characters to split a string in lexems and expected tokens and their types. I learned lexing and tokenizing strings.
