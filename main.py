from parser import *
from interpreter import *

if __name__ == "__main__":
    p = Parser()
    s = "(cdr (list 1 turkey 3 b))"
    print s
    tokens = p.tokenizeInput(s)
    print p.createSublists(tokens)
    i = Interpreter()
    result = i.interpret(p.createSublists(tokens))
    print p.convertToParens(result)
