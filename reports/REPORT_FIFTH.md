# Parser & Building an Abstract Syntax Tree

### Course: Formal Languages & Finite Automata

### Author: Luchianov Vladimir

---

## Theory

A parser is a component of a compiler or interpreter that analyzes the structure of a program or a piece of code according to a given grammar. Its primary task is to validate the syntax of the code and construct a data structure called an Abstract Syntax Tree (AST) that represents the hierarchical structure of the code.

An Abstract Syntax Tree (AST) is a tree-like representation of the structure of a program. It captures the syntax and organization of the code in a way that is more suitable for analysis and interpretation by the compiler or interpreter. Each node in the AST corresponds to a construct in the code, such as statements, expressions, function calls, etc. The nodes are connected through parent-child relationships, reflecting the nesting and hierarchical nature of the code.

Building an AST typically involves a two-step process: lexical analysis and syntactic analysis.

Lexical analysis: Also known as tokenization, this step breaks the input code into individual tokens, such as identifiers, keywords, operators, literals, etc. These tokens are the building blocks for constructing the AST.

Syntactic analysis: This step involves parsing the tokens according to a specified grammar or set of rules. The parser analyzes the sequence and arrangement of tokens to determine if they form valid expressions, statements, or other program constructs. During this process, the parser constructs the AST by creating nodes and establishing their relationships based on the grammar rules.

The resulting AST provides a higher-level representation of the code, abstracting away low-level details. It facilitates various program analyses and transformations, such as type checking, optimization, code generation, and interpretation.

Building an AST is a fundamental step in many language processing tasks, including compilers, interpreters, static analyzers, linters, and code editors. It enables the understanding and manipulation of code structures in a more organized and manageable way.

## Objectives:

1. Get familiar with parsing, what it is and how it can be programmed [1].
2. Get familiar with the concept of AST [2].
3. In addition to what has been done in the 3rd lab work do the following:
   1. In case you didn't have a type that denotes the possible types of tokens you need to:
      1. Have a type **_TokenType_** (like an enum) that can be used in the lexical analysis to categorize the tokens.
      2. Please use regular expressions to identify the type of the token.
   2. Implement the necessary data structures for an AST that could be used for the text you have processed in the 3rd lab work.
   3. Implement a simple parser program that could extract the syntactic information from the input text.

## Implementation description

First thing I've done in this lab was fixing a small issue with lexer. Previously it was ignoring strings isolated with quotes ", but after the fix lexer takes entire string is a token.

```
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
```

```
#Piece of output
('"', 'quot'), ('%d%d%d%d%d%d', 'string'), ('"', 'quot')
```

Second thing after learning about AST was making such structure and creating an instance of it. **AST** object consists of **ASTNode** objects which have such attributes as _name_ and _type_ of string type and _children_ of list type.

```
class ASTNode:
    def __init__(self, tuple):
        type, name = tuple
        self.type = type
        self.name = name
        self.children = []
```

**AST** object itself contains only one method which process taken for example list of tokens and returns root **ASTNode** object.

```
class AST:
    def ast(self, tokens):
        root = ASTNode(("Code", "Block"))
        current_node = root
        new_node = ASTNode(tokens[0])
        current_node.children.append(new_node)
        current_node = new_node
        new_node = ASTNode(tokens[1])
        current_node.children.append(new_node)
        new_node = ASTNode(("Arguments", "Arguments"))
        current_node.children.append(new_node)
        new_node = ASTNode(tokens[len(tokens) - 2])
        current_node.children.append(new_node)
        current_node = current_node.children[1]
        for index in range(2, len(tokens) - 1):
            current_node.children.append(ASTNode(tokens[index]))

        return root
```

Drive code running and testing AST functionality consists of creating an **AST** object and calling its method with arguments preprocessed by lexer.

```
astObj = AST()
ast = astObj.ast(lexemes[1])
```

To obtain results a small helper function was created and ran

```
def printNodes(node, depth=0):
    print('\t' * depth + node.type)
    for child in node.children:
        printNodes(child, depth + 1)

printNodes(ast)
```

And as can be observed data given by lexer

```
[('scanf', 'fun'), ('(', 'round'), ('"', 'quot'), ('%d%d%d%d%d%d', 'string'), ('"', 'quot'), ('', 'string'), (',', 'separator'), ('&', 'oper'), ('work_interval_count', 'identifier'), (',', 'separator'), ('&', 'oper'), ('mode1', 'identifier'), (',', 'separator'), ('&', 'oper'), ('mode2', 'identifier'), (',', 'separator'), ('&', 'oper'), ('mode3', 'identifier'), (',',
'separator'), ('&', 'oper'), ('afk1', 'identifier'), (',', 'separator'), ('&', 'oper'), ('afk2', 'identifier'), (')', 'round'), (';', 'separator')]
```

was transformed into an Abstract Syntax Tree

```
Code
        scanf
                (
                Arguments
                        "
                        %d%d%d%d%d%d
                        "

                        ,
                        &
                        work_interval_count
                        ,
                        &
                        mode1
                        ,
                        &
                        mode2
                        ,
                        &
                        mode3
                        ,
                        &
                        afk1
                        ,
                        &
                        afk2
                        )
                )
```

Third thing I've done during this laboratory work wasn't as successful as previous steps. The initial goal to maintain any transformation of C code into an Abstract Syntax Tree happened to be unreachable, so I minimized it to maintain three different types of operations in C languages. These operations are variable declaration, variable assignment and function call. **Parser** object has a method, which requires a string of C code and returns string itself and message about string allowance in a tuple. The message depends on which of allowed formats was convenient for given string:

```
    if re.match(assignment_pattern, input_string):
            tuple.append("Accepted: Simple Assignment")
        elif re.match(declaration_pattern, input_string):
            tuple.append("Accepted: Declaration")
        elif re.match(function_call_pattern, input_string):
            tuple.append("Accepted: Function Call")
        else:
            tuple.append("Not Accepted")
```

Regular expressions used to define code string allowance are shown below:

```
        assignment_pattern = r'^[a-zA-Z_]\w*\s*=\s*.+;$'
        declaration_pattern = r'^[a-zA-Z_]\w*\s+[a-zA-Z_]\w*;$'
        function_call_pattern = r'^[a-zA-Z_]\w*\s*\(.*\);$'
```

Drive code testing this class begins with creating such object:

```
parser = Parser()
```

And showing results of calling its method in output:

```
print(parser.analyze_c_string("catastrophe();"))

print(parser.analyze_c_string("catastrophe(cata);"))

print(parser.analyze_c_string("int main;"))

print(parser.analyze_c_string("x = 10000 * 200456;"))

print(parser.analyze_c_string("int x = 10000 * 200456;"))
```

Which gives us clear and simple information about the string:

```
['catastrophe();', 'Accepted: Function Call']
['catastrophe(cata);', 'Accepted: Function Call']
['int main;', 'Accepted: Declaration']
['x = 10000 * 200456;', 'Accepted: Simple Assignment']
['int x = 10000 * 200456;', 'Not Accepted']
```

## Conclusions / Screenshots / Results

In this laboratory work I learned about Parsing and Abstract Syntax tree. I improved lexer class by adding strings adaptivity. I added functionality for conversion lexer's output in an AST. I implemented parser with minimized functionality and checked all outputs. I enjoyed learning about syntactic analysis and implementing partial functionality.
