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
            "'": lambda x: x,
            'car': lambda x: x[0],
            'cdr': lambda x: x[1:],
            'cons': lambda x, y: [x] + y,
            'equal?': op.eq,
            'null?': lambda x: x == [],
        })
        return mapper

    # evaluates the specified scheme expression
    def interpret(self, tokens):
        if isinstance(tokens, str):
            return self.mapper[tokens]
        elif not isinstance(tokens, list):
            return tokens
        elif tokens[0] == "'":
            (_, expression) = tokens
            return expression
        else:
            process = self.interpret(tokens[0])
            args = [self.interpret(token) for token in tokens[1:]]
            return process(*args)

