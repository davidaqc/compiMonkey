import ply3.ply.lex as lex
import exceptions

reserved = {
    'if': 'IF',
    'else': 'ELSE',
    'for': 'FOR',
    'in': 'IN',
    'times': 'TIMES',
    'until': 'UNTIL',
    'ret': 'RETURN',

    'turn': 'TURN',
    'turnTo': 'TURNTO',
    'left': 'LEFT',
    'right': 'RIGHT',
    'step' : 'STEP',

    'turtle': 'TURTLE',
    'turtles': 'TURTLES',
    'banana': 'BANANA',
    'bananas': 'BANANAS',
    'crocodile': 'CROCODILE',
    'crocodiles': 'CROCODILES',
    'match': 'MATCH',
    'matches': 'MATCHES',
    'beaver': 'BEAVER',
    'beavers': 'BEAVERS',

    'and': 'AND',
    'or': 'OR',
    'not': 'NOT',

    'distanceTo': 'DISTANCETO',
    'near': 'NEAR',
    'sleeping': 'SLEEPING',
    'health': 'HEALTH',
    'see': 'SEE',
    'say': 'SAY',
}

tokens = [
    'EQUALS',
    'IDENTIFIER',
    'NUM_INT',
    'LPAREN',
    'RPAREN',
    'COMMA',
    'NEWLINE',
    'LSQBRACK',
    'RSQBRACK',
    'ARROW_LTR',
    'POINT',
    'EQ',
    'GT',
    'LT',
    'WS',
    'PLUS',
    'MINUS',
    'MUL',    
    'TRUE',
    'FALSE',
] + list(reserved.values())

t_COMMA = ','
t_EQUALS = '='
t_PLUS = r'\+'
t_MINUS = '-'
t_MUL = r'\*'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LSQBRACK = r'\['
t_RSQBRACK = r'\]'
t_ARROW_LTR = '->'
t_ignore_COMMENTS = r'//.+'
t_POINT = r'\.'
t_EQ = '=='
t_GT = '>'
t_LT = '<'

def t_NEWLINE(t):
    r'\n'
    t.lexer.lineno += 1
    t.lexer.linepos = 0
    pass

def t_WS(t):
    r'[ \t]+'

    if t.value == " ":
        tab = len(t.value) % 5
    else:
        tab = 0

    if tab == 0:
        pass
        #return t
    else:
        pass

def t_TRUE(t):
    'true'
    t.value = True
    return t

def t_FALSE(t):
    'false'
    t.value = False
    return t

def t_IDENTIFIER(t):
    r'[a-z][a-zA-Z@$?]*'
    t.type = reserved.get(t.value, t.type)
    return t

def t_NUM_INT(t):
    r'-?\d+'
    t.value = int(t.value)
    return t

def t_error(t):
    print ("Error Lexico!!!")
    raise exceptions.UnexpectedCharacter("Unexpected character '%s' at line %d" % (t.value[0], t.lineno))

lexer = lex.lex()

"""fp = open("resources/code.txt", "r")
source = fp.read()
fp.close()
lexer.input(source)
# Tokenize
while True:
    tok = lexer.token()
    if not tok:
        break      # No more input
    print(tok)"""
