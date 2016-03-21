from parser import *
from interpreter import *

if __name__ == "__main__":
    p = Parser()
    s = "(* -5 (- 5 6))"
    print s
    tokens = p.tokenizeInput(s)
    print p.createSublists(tokens)
    i = Interpreter()
    print i.interpret(p.createSublists(tokens))
