import math
import operator as op

class Interpreter:

    def __init__(self):
        self.mapper = self.tokenMapper()

    # maps potential scheme variables to their values
    def tokenMapper(self):
        mapper = dict()
        mapper.update(vars(math)) # adds functions like sin, cos, etc
        mapper.update({
            '+': op.add,
            '-': op.sub,
            '*': op.mul,
            '/': op.div,
            '<': op.lt,
            '<=': op.le,
            '>': op.gt,
            '>=': op.ge,
            '=': op.eq,
            'car': lambda x: x[0],
            'cdr': lambda x: x[1:],
            'cons': lambda x, y: [x] + y,
            'equal?': op.eq,
            'list': lambda *x: [symbol for symbol in x],
            'list?': lambda x: isinstance(x, list),
            'null?': lambda x: x == [],
            'number?': lambda x: x == int(x) or x == float(x)
        })
        return mapper

    # evaluates the specified scheme expression
    def interpret(self, tokens):
        # checks if tokens is a built in scheme function
        if tokens in self.mapper.keys():
            return self.mapper[tokens]
        # checks if tokens is a literal
        elif not isinstance(tokens, list):
            return tokens
        # ignores the quote and interprets the rest as a literal expression
        elif tokens[0] == "'":
            (_, expression) = tokens
            return expression
        # defines a new scheme function
        elif tokens[0] == 'define':
            (_, variable, value) = tokens
            self.mapper[variable] = self.interpret(value)
        elif tokens[0] == 'display':
            if len(tokens) > 2:
                raise InterpretError("Too many arguments passed to display")
            (_, expression) = tokens
            return self.interpret(expression)
        # splits tokens into the scheme function and its arugments
        else:
            process = self.interpret(tokens[0])
            args = [self.interpret(token) for token in tokens[1:]]
            return process(*args)

class InterpretError(Exception):
    pass
