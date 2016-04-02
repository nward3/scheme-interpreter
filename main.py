import sys
from parser import *
from interpreter import *

if __name__ == "__main__":
    interpreter = Interpreter()
    parser = Parser()

    # function that processes code using parser and interpreter modules
    def interpretExpression(code):
        # parse the input
        tokensSublists = parser.parse(code)

        # pass the sublists of tokens (structure mirrors the levels of parens in
        # scheme code) to the interpreter
        result = interpreter.interpret(tokensSublists)
        return parser.convertToParens(result)

    if len(sys.argv) > 2:
        print "Please specify the scheme file to run"
        print "Example usage: python main.py [code.scm]"

        sys.exit(1)

    # if file was specified to interpret
    elif len(sys.argv) == 2:
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

        try:
            print interpretExpression(s)
        except ParseError as ex:
            print ex

    # interactive mode
    elif len(sys.argv) == 1:
        # prompt user for input until user presses ctrl+c or ctrl+d
        while(True):
            try:
                sys.stdout.write('>> ')
                code = raw_input()
                result = interpretExpression(code)
                if result != None:
                    print result
            except EOFError:
                sys.exit(0)
            except KeyboardInterrupt:
                sys.exit(0)
            except ParseError as ex:
                print ex
