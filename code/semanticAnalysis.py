import operator
from types import LambdaType
from exceptions import *
import symbol_table
import global_variable

symbols = symbol_table.SymbolTable()

class InstructionList:
    def __init__(self, children=None):

        if children is None:
            children = []
        self.children = children

    def __len__(self):
        return len(self.children)

    def __iter__(self):
        return iter(self.children)

    def __repr__(self):
        return '<InstructionList {0}>'.format(self.children)

    def eval(self):
        """
        Evaluates all the class children and returns the result
        of their eval method in a list or returns an ExitStatement
        in case one is found
        """
        ret = []
        for n in self:

            if isinstance(n, ExitStatement):
                return n

            if isinstance(n, Turn):
                aux_list = []
                if (isinstance(n.name, str)) and (isinstance(n.index, str)):
                    global_variable.instructions_list.append(n.name)
                elif(isinstance(n.name, Identifier) and isinstance(n.index, Identifier)):
                    aux_list = ["turnTo", "crocodile", n.name.eval(), n.index.eval()]
                    global_variable.instructions_list.append(aux_list)
                elif(isinstance(n.name, Identifier)):
                    aux_list = ["turnTo", "desconocido", n.name.eval()]
                    global_variable.instructions_list.append(aux_list)
                elif (isinstance(n.index, int)):
                    aux_list = ["turnTo", n.name, n.index]
                    global_variable.instructions_list.append(aux_list)
                elif (isinstance(n.name, str)):
                    aux_list = ["turnTo", n.name, n.index.eval()]
                    global_variable.instructions_list.append(aux_list)

            if isinstance(n, Step):
                aux_list = []
                if (isinstance(n.steps, int)):
                    aux_list = [n.name.eval(), n.character, n.steps]
                    global_variable.instructions_list.append(aux_list)
                elif  (isinstance(n.steps, Identifier)) and (isinstance(n.name, Identifier)):               
                    aux_list = [n.name.eval(), "turtle", n.steps.eval()]
                    global_variable.instructions_list.append(aux_list)
                elif (isinstance(n.steps, Primitive)):
                    aux_list = [n.name.eval(), "turtle", n.steps.eval()]
                    global_variable.instructions_list.append(aux_list)
                else:
                    if n.steps == "Minus":
                        aux_list = [n.name.eval()*-1, n.character]
                    else:
                        aux_list = [n.name.eval(), n.character]
                    global_variable.instructions_list.append(aux_list)

            if isinstance(n, PrintStatement):
                global_variable.instructions_list.append(n.function_type)

            res = n.eval()

            if isinstance(res, ExitStatement):
                return res
            elif res is not None:
                ret.append(res)

        return ret

class BaseExpression:
    def eval(self):
        raise NotImplementedError()

class ExitStatement(BaseExpression):
    def __iter__(self):
        return []

    def eval(self):
        pass

class ReturnStatement(ExitStatement):
    def __init__(self, expr: BaseExpression):
        self.expr = expr

    def __repr__(self):
        return '<Return expr={0}>'.format(self.expr)

    def eval(self):
        return full_eval(self.expr)

def full_eval(expr: BaseExpression):
    """
    Fully evaluates the passex expression returning it's value
    """
    while isinstance(expr, BaseExpression):
        expr = expr.eval()

    return expr

class Primitive(BaseExpression):
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return '<Primitive "{0}"({1})>'.format(self.value, self.value.__class__)

    def eval(self):
        return self.value

class Identifier(BaseExpression):
    is_function = False

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Identifier {0}>'.format(self.name)

    def assign(self, val):
        if self.is_function:
            symbols.set_func(self.name, val)
        else:
            symbols.set_sym(self.name, val)

    def eval(self):
        if self.is_function:
            return symbols.get_func(self.name)

        return symbols.get_sym(self.name)

class Turn(BaseExpression):

    def __init__(self, name, index):
        self.name = name
        self.index = index

    def __repr__(self):
        return '<Identifier {0}>'.format(self.name)

    def eval(self):
        if(isinstance(self.name, Identifier)):
            return self.name.eval()
        elif(isinstance(self.index, str)):
            return self.name
        else:
            if(isinstance(self.index, Identifier)):
                return ("turnTo", self.name, self.index.eval())
            else:
                return ("turnTo", self.name, self.index)

class Step(BaseExpression):

    def __init__(self, name, character, steps):
        self.name = name
        self.character = character
        self.steps = steps

    def __repr__(self):
        return '<Identifier {0}>'.format(self.name)

    def eval(self):
        if (isinstance(self.steps, int)):
            return (self.name.eval(), self.character, self.steps)
        elif (isinstance(self.steps, Identifier)) and (isinstance(self.name, Identifier)):
            return (self.name.eval(), self.character, self.steps.eval())
        elif (isinstance(self.name, Identifier)) and self.steps == "Minus":
            return (self.name.eval()*-1, self.character)
        elif (isinstance(self.name, Identifier)):
            return (self.name.eval(), self.character)
        elif (isinstance(self.name, int)):
            return (self.name, self.character)
        elif(isinstance(self.character, str)):
            return (self.name.eval(), self.character)
        else:
            return (self.name.eval(), self.character.eval())

class Array(BaseExpression):
    def __init__(self, values: InstructionList):
        self.values = values

    def __repr__(self):
        return '<Array len={0} items={1}>'.format(len(self.values.children), self.values)

    def eval(self):
        return self.values.eval()

class ArrayAccess(BaseExpression):
    def __init__(self, array: Identifier, index: BaseExpression):
        self.array = array
        self.index = index

    def __repr__(self):
        return '<Array index={0}>'.format(self.index)

    def eval(self):
        return self.array.eval()[self.index.eval()]

class ArrayAssign(BaseExpression):
    def __init__(self, array: Identifier, index: BaseExpression, value: BaseExpression):
        self.array = array
        self.index = index
        self.value = value

    def __repr__(self):
        return '<Array arr={0} index={1} value={2}>'.format(self.array, self.index, self.value)

    def eval(self):
        self.array.eval()[self.index.eval()] = self.value.eval()

class Assignment(BaseExpression):
    def __init__(self, identifier: Identifier, val):
        self.identifier = identifier
        self.val = val

    def __repr__(self):
        return '<Assignment sym={0}; val={1}>'.format(self.identifier, self.val)

    def eval(self):
        if self.identifier.is_function:
            self.identifier.assign(self.val)
        else:
            self.identifier.assign(self.val.eval())
            
class BinaryOperation(BaseExpression):
    __operations = {
        '+': operator.add,
        '-': operator.sub,
        '>': operator.gt,
        '<': operator.lt,
        '==': operator.eq,

        'and': lambda a, b: a.eval() and b.eval(),
        'or': lambda a, b: a.eval() or b.eval(),
    }

    def __repr__(self):
        return '<BinaryOperation left ={0} right={1} operation="{2}">'.format(self.left, self.right, self.op)

    def __init__(self, left, right, op):
        self.left = left
        self.right = right
        self.op = op

    def eval(self):
        left = None
        right = None

        try:
            # find the operation that needs to be performed
            op = self.__operations[self.op]

            # The only lambda operations are logical and/or
            # Pass the arguments unevaluated as they will be during the lambda execution
            # This implements short circuit boolean evaluation
            if isinstance(op, LambdaType):
                return op(self.left, self.right)

            # otherwise, straight up call the operation, also save the variables
            # in case they are to be used for the exception block
            left = self.left.eval()
            right = self.right.eval()
            return op(left, right)
        except TypeError:
            fmt = (left.__class__.__name__, left, self.op, right.__class__.__name__, right)
            raise InterpreterRuntimeError("Unable to apply operation (%s: %s) %s (%s: %s)" % fmt)

class UnaryOperation(BaseExpression):
    __operations = {
        'not': operator.not_
    }

    def __repr__(self):
        return '<Unary operation: operation={0} expr={1}>'.format(self.operation, self.expr)

    def __init__(self, operation, expr: BaseExpression):
        self.operation = operation
        self.expr = expr

    def eval(self):
        return self.__operations[self.operation](self.expr.eval())

class If(BaseExpression):
    def __init__(self, condition: BaseExpression, truepart: InstructionList, elsepart=None):
        self.condition = condition
        self.truepart = truepart
        self.elsepart = elsepart

    def __repr__(self):
        return '<If condition={0} then={1} else={2}>'.format(self.condition, self.truepart, self.elsepart)

    def eval(self):
        if self.condition.eval():
            return self.truepart.eval()
        elif self.elsepart is not None:
            return self.elsepart.eval()

class Times(BaseExpression):
    def __init__(self, variable: Identifier, end: Primitive, body: InstructionList):
        self.variable = variable
        self.start = 1
        self.end = end
        self.body = body

    def __repr__(self):
        fmt = '<For start={0} end={1} body={2}>'
        return fmt.format(self.start, self.end, self.body)

    def eval(self):
        lo = self.start
        hi = self.end.eval() + 1
        sign = 1

        for i in range(lo, hi, sign):
            self.variable.assign(i)

            # in case of exit statement prematurely break the loop
            if isinstance(self.body.eval(), ExitStatement):
                break

class ForIn(BaseExpression):
    def __init__(self, variable: Identifier, type_avatar, body: InstructionList):
        self.variable = variable
        self.type_avatar = type_avatar
        self.body = body

    def __repr__(self):
        return '<ForIn var={0} in iterable={1} do body={2}>'.format(self.variable, self.type_avatar, self.body)

    def eval(self):
        if self.type_avatar == "bananas" and global_variable.bananas_type[0] == "bananas":
            for i in global_variable.bananas_list:
                self.variable.assign(i)
                if isinstance(self.body.eval(), ExitStatement):
                    break
        elif self.type_avatar == "turtles" and global_variable.turtles_type[0] == "turtles":
            for i in global_variable.turtles_list:
                self.variable.assign(i)
                if isinstance(self.body.eval(), ExitStatement):
                    break
        elif self.type_avatar == "crocodiles" and global_variable.crocodiles_type[0] == "crocodiles":
            for i in global_variable.crocodiles_list:
                self.variable.assign(i)
                if isinstance(self.body.eval(), ExitStatement):
                    break
        elif self.type_avatar == "matches" and global_variable.matches_type[0] == "matches":
            for i in global_variable.matches_list:
                self.variable.assign(i)
                if isinstance(self.body.eval(), ExitStatement):
                    break

class Until(BaseExpression):
    def __init__(self, condition, body, variable: Identifier):
        self.condition = condition
        self.body = body
        self.variable = variable

    def __repr__(self):
        return '<While cond={0} body={1}>'.format(self.condition, self.body)

    def eval(self):
        if isinstance(self.condition, str):
            salir = True
            contador = 1
            while salir:
                contador += 1
                for i in self.body.eval():
                    if isinstance(i, tuple):
                        if i[1] == "Monkey":
                            if (global_variable.condition_until[4] == 0):
                                global_variable.condition_until[1] = global_variable.condition_until[1] - (i[0] * 10)
                            elif (global_variable.condition_until[4] == 1):
                                global_variable.condition_until[0] = global_variable.condition_until[0] - (i[0] * 10)
                            elif (global_variable.condition_until[4] == 2):
                                global_variable.condition_until[1] = global_variable.condition_until[1] + (i[0] * 10)
                            else:
                                global_variable.condition_until[0] = global_variable.condition_until[0] + (i[0] * 10)
                            dif_x = abs(global_variable.condition_until[0] - global_variable.condition_until[2])
                            dif_y = abs(global_variable.condition_until[1] - global_variable.condition_until[3])
                            if dif_x < 200 and dif_y < 200:
                                salir = False
                    elif i == "left":
                        if (global_variable.condition_until[4] == 0):
                            global_variable.condition_until[4] = 1
                        elif (global_variable.condition_until[4] == 1):
                            global_variable.condition_until[4] = 2
                        elif (global_variable.condition_until[4] == 2):
                            global_variable.condition_until[4] = 3
                        else:
                            global_variable.condition_until[4] = 0
                    elif i == "right":
                        if (global_variable.condition_until[4] == 0):
                            global_variable.condition_until[4] = 3
                        elif (global_variable.condition_until[4] == 1):
                            global_variable.condition_until[4] = 0
                        elif (global_variable.condition_until[4] == 2):
                            global_variable.condition_until[4] = 1
                        else:
                            global_variable.condition_until[4] = 2
                #if contador > 100:
                #    break
                    
        else:
            while self.condition.eval():
                if isinstance(self.body.eval(), ExitStatement):
                    break

class PrintStatement(BaseExpression):
    def __init__(self, function_type):
        self.function_type = function_type

    def __repr__(self):
        return '<Print {0}>'.format(self.function_type)

    def eval(self):
        return self.function_type

class FunctionCall(BaseExpression):
    def __init__(self, name: Identifier, params: InstructionList):
        self.name = name
        self.params = params

    def __repr__(self):
        return '<Function call name={0} params={1}>'.format(self.name, self.params)

    def __eval_builtin_func(self):
        func = self.name.eval()
        args = []

        for p in self.params:
            args.append(full_eval(p))

        return func.eval(args)

    def __eval_udf(self):
        func = self.name.eval()
        args = {}

        # check param count
        l1 = len(func.params)
        l2 = len(self.params)

        if l1 != l2:
            msg = "Invalid number of arguments for function {0}. Expected {1} got {2}"
            raise InvalidParamCount(msg.format(self.name.name, l1, l2))

        # pair the defined parameters in the function signature with
        # whatever is being passed on.
        #
        # On the parameters we only need the name rather than fully evaluating them
        for p, v in zip(func.params, self.params):
            args[p.name] = full_eval(v)

        return func.eval(args)

    def eval(self):
        if isinstance(self.name.eval(), BuiltInFunction):
            return self.__eval_builtin_func()

        return self.__eval_udf()

class Function(BaseExpression):
    def __init__(self, params: InstructionList, body: InstructionList):
        self.params = params
        self.body = body

    def __repr__(self):
        return '<Function params={0} body={1}>'.format(self.params, self.body)

    def eval(self, args):
        symbols.set_local(True)

        for k, v in args.items():
            symbols.set_sym(k, v)

        try:
            ret = self.body.eval()

            if isinstance(ret, ReturnStatement):
                return ret.eval()
        finally:
            symbols.set_local(False)

        return None

class BuiltInFunction(BaseExpression):
    def __init__(self, func):
        self.func = func

    def __repr__(self):
        return '<Builtin function {0}>'.format(self.func)

    def eval(self, args):
        return self.func(*args)