import ply3.ply.yacc as yacc
import semanticAnalysis as ast
from lexicalAnalysis import *
from exceptions import *
import global_variable

precedence = (
    ('left', 'PLUS', 'MINUS'),
    ('left', 'OR', 'AND'),
)

def p_statement_list(p):
    '''
    statement_list : statement
                   | statement_list statement
    '''
    if len(p) == 2:
        p[0] = ast.InstructionList([p[1]])
    else:
        p[1].children.append(p[2])
        p[0] = p[1]

def p_statement(p):
    '''
    statement : identifier
              | expression
              | if_statement
              | turn
              | step
    '''
    p[0] = p[1]

def p_turn(p):
    '''
    turn : TURN LEFT
        | TURN RIGHT
        | TURN NUM_INT
        | expression POINT TURNTO expression
        | TURNTO BANANA LSQBRACK NUM_INT RSQBRACK
        | TURNTO BANANA LSQBRACK expression RSQBRACK
        | TURNTO MATCH LSQBRACK NUM_INT RSQBRACK
        | TURNTO MATCH LSQBRACK expression RSQBRACK
        | TURNTO expression
    '''
    if len(p) == 3:
        p[0] = ast.Turn(p[2], "")
    elif len(p) == 5:
        p[0] = ast.Turn(p[1], p[4])
    else:
        p[0] = ast.Turn(p[2], p[4])

def p_step(p):
    '''
    step :  STEP expression
        | STEP MINUS expression
        | STEP DISTANCETO expression
        | expression POINT STEP expression
        | BEAVER LSQBRACK NUM_INT RSQBRACK POINT STEP expression
        | TURTLE LSQBRACK NUM_INT RSQBRACK POINT STEP expression
        | STEP DISTANCETO BANANA LSQBRACK NUM_INT RSQBRACK
        | STEP DISTANCETO BANANA LSQBRACK expression RSQBRACK
        | STEP DISTANCETO MATCH LSQBRACK NUM_INT RSQBRACK
        | STEP DISTANCETO MATCH LSQBRACK expression RSQBRACK
    '''
    if (len(p)) == 3:
        p[0] = ast.Step(p[2], "Monkey", "")
    elif (len(p)) == 4 and p[2] == "-":
        p[0] = ast.Step(p[3], "Monkey", "Minus")
    elif (len(p)) == 4:
        p[0] = ast.Step(p[3], "Desconocido", "")
    elif (len(p)) == 5:
        p[0] = ast.Step(p[1], "Desconocido", p[4])
    elif (len(p)) == 8:
        if p[1] == "beaver":
            p[0] = ast.Step(p[7], "Beaver", p[3])
        elif p[1] == "turtle":
            p[0] = ast.Step(p[7], "Turtle", p[3])
    else:
        p[0] = ast.Step(p[5], p[3], "")

def p_identifier(p):
    '''
    identifier : IDENTIFIER
    '''
    p[0] = ast.Identifier(p[1])

def p_primitive(p):
    '''
    primitive : NUM_INT
              | boolean
    '''
    if isinstance(p[1], ast.BaseExpression):
        p[0] = p[1]
    else:
        p[0] = ast.Primitive(p[1])

def p_binary_op(p):
    '''
    expression : expression PLUS expression %prec PLUS
               | expression MINUS expression %prec MINUS
    '''
    p[0] = ast.BinaryOperation(p[1], p[3], p[2])

def p_boolean_operators(p):
    '''
    boolean : boolean AND boolean
            | boolean OR boolean
            | expression EQ expression
            | expression GT expression
            | expression LT expression
    '''
    p[0] = ast.BinaryOperation(p[1], p[3], p[2])

def p_unary_operation(p):
    '''
    expression : NOT expression
    '''
    p[0] = ast.UnaryOperation(p[1], p[2])

def p_boolean(p):
    '''
    boolean : TRUE
            | FALSE
    '''
    p[0] = ast.Primitive(p[1])

def p_assignable(p):
    '''
    assignable : primitive
               | expression
    '''
    p[0] = p[1]

def p_comma_separated_expr(p):
    '''
    arguments : arguments COMMA expression
              | expression
              |
    '''
    if len(p) == 2:
        p[0] = ast.InstructionList([p[1]])
    elif len(p) == 1:
        p[0] = ast.InstructionList()
    else:
        p[1].children.append(p[3])
        p[0] = p[1]

def p_arrays(p):
    '''
    expression : LSQBRACK arguments RSQBRACK
    '''
    p[0] = ast.Array(p[2])

def p_array_access(p):
    '''
    expression : identifier LSQBRACK expression RSQBRACK
    '''
    p[0] = ast.ArrayAccess(p[1], p[3])

def p_array_access_assign(p):
    '''
    statement : identifier LSQBRACK expression RSQBRACK EQUALS expression
    '''
    p[0] = ast.ArrayAssign(p[1], p[3], p[6])

def p_assign(p):
    '''
    expression : identifier EQUALS assignable
    '''
    p[0] = ast.Assignment(p[1], p[3])

def p_ifstatement(p):
    '''
    if_statement : IF expression statement_list COMMA
    '''
    p[0] = ast.If(p[2], p[3])

def p_ifstatement_else(p):
    '''
    if_statement : IF expression statement_list ELSE statement_list COMMA
    '''
    p[0] = ast.If(p[2], p[3], p[5])

def p_print_statement(p):
    '''
    statement : SAY LPAREN RPAREN
              | SEE LPAREN RPAREN
              | HEALTH LPAREN RPAREN
    '''
    p[0] = ast.PrintStatement(p[1])

def p_expression(p):
    '''
    expression : primitive
               | identifier
    '''
    p[0] = p[1]

def p_times(p):
    '''
    statement : expression POINT TIMES ARROW_LTR statement_list COMMA
    '''
    i = 0
    p[0] = ast.Times(ast.Identifier(i), p[1], p[5])

def p_for_in_loop(p):
    '''
    statement : FOR identifier IN BANANAS statement_list COMMA
              | FOR identifier IN TURTLES statement_list COMMA
              | FOR identifier IN CROCODILES statement_list COMMA
              | FOR identifier IN MATCHES statement_list COMMA
    '''
    p[0] = ast.ForIn(p[2], p[4], p[5])

def p_until_loop(p):
    '''
    statement : UNTIL expression statement_list COMMA
              | UNTIL NEAR MATCH statement_list COMMA
    '''
    if len(p) == 5:
        p[0] = ast.Until(p[2], p[3], "")
    else:
        p[0] = ast.Until("", p[4], p[3])

def p_function_declaration(p):
    '''
    statement : identifier EQUALS LPAREN arguments RPAREN ARROW_LTR statement_list COMMA
    '''
    p[1].is_function = True

    p[0] = ast.Assignment(p[1], ast.Function(p[4], p[7]))

def p_return(p):
    '''
    statement : RETURN expression
    '''
    p[0] = ast.ReturnStatement(p[2])

def p_function_call(p):
    '''
    expression : identifier LPAREN arguments RPAREN
    statement : identifier arguments COMMA

    '''
    p[1].is_function = True

    if len(p) == 4:
        p[0] = ast.FunctionCall(p[1], p[2])
    else:
        p[0] = ast.FunctionCall(p[1], p[3])

def p_error(p):
    print("Error Sintactico!!!")
    if p is not None:
        raise ParserSyntaxError(
            "Syntax error at line %d, illegal token '%s' found" % (p.lineno, p.value))

    raise ParserSyntaxError("Unexpected end of input")

def get_parser():
    return yacc.yacc()
