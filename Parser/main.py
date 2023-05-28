from lexer import Lexer
from AST import AST
from parser_1 import Parser

lexer = Lexer(({'types' : ['int', 'bool', 'char'],
                'separator' : [',', ';'],
                'round' : ['(', ')'],
                'square' : ['[', ']'],
                'curly' : ['{', '}'],
                'quot' : ['"', '"'],
                'oper' : ['&', '*'],
                'eq' : ['='],
                'fun' : ['scanf', 'printf']},
                [';']))

lexemes = lexer.lexing('''int work_interval_count , mode1 , mode2 , mode3 , afk1 , afk2 ;
scanf ( " %d %d %d %d %d %d " , & work_interval_count , & mode1 , & mode2 , & mode3 , & afk1 , & afk2 ) ;
works = ( int * ) ;''')

for lexeme in lexemes:
    print(lexeme)

astObj = AST()
ast = astObj.ast(lexemes[1])

def printNodes(node, depth=0):
    print('\t' * depth + node.type)
    for child in node.children:
        printNodes(child, depth + 1)

printNodes(ast)

#Parser check
parser = Parser()

print(parser.analyze_c_string("catastrophe();"))

print(parser.analyze_c_string("catastrophe(cata);"))

print(parser.analyze_c_string("int main;"))

print(parser.analyze_c_string("x = 10000 * 200456;"))

print(parser.analyze_c_string("int x = 10000 * 200456;"))