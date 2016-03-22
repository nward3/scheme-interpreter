import sys
from parser import *
from interpreter import *

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print "Please specify the scheme file to run"
        print "Example usage: python main.py [code.scm]"

        sys.exit(1)

    # open file and save the contents into string s
    filename = sys.argv[1]
    s = str()
    try:
        with open(filename, 'r') as f:
            for line in f:
                s = s + line
    except IOError as e:
        print "Unable to open file: " + filename
        sys.exit(1)
    except Exception as ex:
        print e
        sys.exit(1)

    p = Parser()
    i = Interpreter()

    # parse the input
    tokens = p.tokenizeInput(s)
    tokensSublists = p.createSublists(tokens)

    # pass the sublists of tokens (structure mirrors the levels of parens in
    # scheme code) to the interpreter
    result = i.interpret(tokensSublists)
    print p.convertToParens(result)
