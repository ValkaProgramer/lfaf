from lexer import Lexer

lexer = Lexer(({'keywords' : ['int', 'scanf'],
                'separator' : [',', ';', '"', '(', ')'],
                'operator' : ['&', '=', '*']},
                [';']))

print(lexer.lexing('int work_interval_count , mode1 , mode2 , mode3 , afk1 , afk2 ; scanf ( " %d %d %d %d %d %d " , & work_interval_count , & mode1 , & mode2 , & mode3 , & afk1 , & afk2 ) ; works = ( int * ) ;'))