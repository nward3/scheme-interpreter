import sys
from parser import *
from interpreter import *

if __name__ == "__main__":
    interpreter = Interpreter()
    parser = Parser()

    # interpret a list of expressions
    def interpretExpressions(listOfExpressions):
        for expression in listOfExpressions:
            result = interpretExpression(expression)
            if result != None:
                print result

    # function that processes code using parser and interpreter modules
    def interpretExpression(code):
        # parse the input
        tokensSublists = parser.parse(code)

        # pass the sublists of tokens (structure mirrors the levels of parens in
        # scheme code) to the interpreter
        result = interpreter.interpret(tokensSublists)
        return parser.convertToParens(result)

    # try to open the specified file, and return a string with the contents of the file
    # newlines at the end of each line are removed
    def getFileContents(filename):
            # open file and save the contents into string s
            s = str()
            try:
                with open(filename, 'r') as f:
                    for line in f:
                        s = s + line.rstrip()

                return s

            except IOError as e:
                print "Unable to open file: " + filename
                sys.exit(1)
            except Exception as ex:
                print e
                sys.exit(1)

    if len(sys.argv) > 2:
        print "Please specify the scheme file to run"
        print "Example usage: python main.py [code.scm]"

        sys.exit(1)

    # if file was specified to interpret
    elif len(sys.argv) == 2:
        filename = sys.argv[1]
        s = getFileContents(filename)

        try:
            # build up list of expressions to evaluate from the code in the input file
            listOfExpressions = list()
            expression = str()
            for char in s:
                expression += char
                if char == "(" or char == ")":
                    # check if the parens are balanced. if so, current string is a complete expression
                    if parser.hasBalancedParensNoThrow(expression):
                        # add current expression to list of expressions to evaluate
                        listOfExpressions.append(expression)

                        # reset current expression string
                        expression = ""
            
            # add this invalid expression to the list to be evaluated so that the error is displayed
            if expression != "":
                listOfExpressions.append(expression)

            interpretExpressions(listOfExpressions)

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

