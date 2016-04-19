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
        'not': op.not_,
        'null?': lambda x: x == [],
        'number?': lambda x: x == int(x) or x == float(x),
        'else': True
        })
    return mapper

globalEnvironment = tokenMapper()

# evaluate 1st expression in pair of expressions until one is true
# execute 2nd expression for the pair with a true first expression
def executeCond(expressions, env):
    interpreter = Interpreter()

    # improper number of arguments
    if len(expressions) % 2 != 0:
        return InterpretError()

    # create pairs of expressions:
    # 1st expression is truth condition, 2nd expression is expressi2on to evaluate
    for exp1,exp2 in zip(expressions[0::2], expressions[1::2]):
        # improper structure; else clause must be last condition to evaluate
        if exp1 == 'else' and exp1 != expressions[-2]:
            return InterpretError()
        # execute first true condition
        elif interpreter.interpret(exp1, env) == True:
            return interpreter.interpret(exp2, env)

# logical AND: returns true if all expressions are true; false otherwise
def executeAnd(expressions, env):
    interpreter = Interpreter()

    # improper number of arguments
    if len(expressions) < 2:
        return InterpretError()

    # check that every expression is true using short-circuit logic
    for exp in expressions:
        if not interpreter.interpret(exp, env):
            return False

    return True

# logical OR: returns true if any expression is true; false otherwise
def executeOr(expressions, env):
    interpreter = Interpreter()

    # improper number of arguments
    if len(expressions) < 2:
        return InterpretError()

    # check if any expression is true using short-circuit logic
    for exp in expressions:
        if interpreter.interpret(exp, env):
            return True

    return False

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
            env[name] = self.interpret(value, env)
        elif tokens[0] == 'lambda':
            # TODO: check that len(tokens) == 2
            (_, params, functionTemplate) = tokens

            # return a UserFunction that will be called later when the args are passed
            return UserFunction(params, functionTemplate, env)
        # executes expression after first true expression
        elif tokens[0] == 'cond':
            expressions = []
            for token in tokens[1:]:
                for expression in token:
                    expressions.append(expression)
            return executeCond(expressions, env)
        elif tokens[0] == 'and':
            expressions = []
            for expression in tokens[1:]:
                expressions.append(expression)
            return executeAnd(expressions, env)
        elif tokens[0] == 'or':
            expressions = []
            for expression in tokens[1:]:
                expressions.append(expression)
            return executeOr(expressions, env)
        elif tokens[0] == 'display':
            if len(tokens) > 2:
                raise InterpretError("Too many arguments passed to display")
            (_, expression) = tokens
            return self.interpret(expression)
        # splits tokeins into the scheme function and its arugments
        else:
            process = self.interpret(tokens[0], env)
            args = [self.interpret(token, env) for token in tokens[1:]]

            return process(*args)

class InterpretError(Exception):
    pass
