import math
import operator as op

# environment is similar to the current scope
# an environment is a dictionary of {var: value} pairs that has a reference to the parent environment
# with the find method, procedures always have access to the globalEnvironment, the top level
class Environment(dict):
    def __init__(self, params=(), args=(), parent=None):
        # match up each param and arg as key/value pairs
        self.update(zip(params, args))
        self.parent = parent

    def find(self, var):
        # find var in the innermost environment
        # if var is not in an environment, try its parent environment
        # return self if (var in self) else self.parent.find(var)
        if var in self:
            return self
        elif self.parent == None:
            # if var hasn't been found yet and just searched in the globalEnv, var isn't in env
            return None
        else:
            return self.parent.find(var)

# maps potential scheme variables to their values
def tokenMapper():
    mapper = Environment()
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

globalEnvironment = tokenMapper()

class UserFunction(object):
    # save the params, body (function template), and the function's parent environment
    def __init__(self, params, body, parentEnvironment):
        self.params = params
        self.body = body
        self.parentEnvironment = parentEnvironment

    # Evaluate the user function when process(*args) is called in the Interpreter.interpret method
    # passes in the arguments that the UserFunction is invoked with
    def __call__(self, *args):
        interpreter = Interpreter()

        # TODO: expect len(self.params) and len(args) to be the same
        # how to get function name for better error message?

        # create the environment for the function so that the params/args key-value pairs
        # are in scope when the body is evaluated
        functionEnv = Environment(self.params, args, self.parentEnvironment)

        # interpret the args passed to the UserFunction using the functionEnv
        # which has the args in it
        return interpreter.interpret(self.body, functionEnv)

class Interpreter:

    # evaluates the specified scheme expression
    # the global environment will be used except for lambda's
    def interpret(self, tokens, env=globalEnvironment):
        # check for function/variable reference (only if tokens is a string, not a list)
        if isinstance(tokens, str) and env.find(tokens) != None:
            # if tokens is in the env, return its value
            return env.find(tokens)[tokens]
        # checks if tokens is a literal
        elif not isinstance(tokens, list):
            return tokens
        # ignores the quote and interprets the rest as a literal expression
        elif tokens[0] == "'":
            (_, expression) = tokens
            return expression
        # defines a new scheme function
        elif tokens[0] == 'define':
            # TODO: check that len(tokens) == 2
            (_, name, value) = tokens
            env[name] = self.interpret(value)
        elif tokens[0] == 'lambda':
            # TODO: check that len(tokens) == 2
            (_, params, functionTemplate) = tokens

            # return a UserFunction that will be called later when the args are passed
            return UserFunction(params, functionTemplate, env)
        elif tokens[0] == 'display':
            if len(tokens) > 2:
                raise InterpretError("Too many arguments passed to display")
            (_, expression) = tokens
            return self.interpret(expression)
        # splits tokens into the scheme function and its arugments
        else:
            process = self.interpret(tokens[0], env)
            args = [self.interpret(token, env) for token in tokens[1:]]

            return process(*args)

class InterpretError(Exception):
    pass
