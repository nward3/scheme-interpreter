#!/usr/bin/python
import collections

class Parser:

    # input: input file/code
    # output: array of tokens of code
    def tokenizeInput(self, code):
        # add whitespace around parens so they can be split correctly
        code = code.replace("(", " ( ").replace(")", " ) ")
        tokens = list()
        for token in code.split():
            tokens.append(token)

        return tokens

    def createSublists(self, tokens):
        return self.createSublistsHelper(collections.deque(tokens), [])

    def createSublistsHelper(self, tokens, sublists):
        print tokens


if __name__ == "__main__":
    p = Parser()
    s = "(display (eq? 5 a))"
    print s
    tokens = p.tokenizeInput(s)
    p.createSublists(tokens)
