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

    # returns an array of subarrays that mirrors the nested paren structure of scheme
    def createSublists(self, tokens):
        sublists = self.createSublistsHelper(collections.deque(tokens), [])

        # desired contents are nested inside an outer array
        return sublists[0]

    # tokens is a deque for optimized pop(0) operation
    # sublists is a list
    def createSublistsHelper(self, tokens, sublists):
        # base case
        if len(tokens) == 0:
            # no tokens left
            print "here"
            return sublists

        # get next token and remove remove the token that is being processed from the deque of tokens to process
        token = tokens.popleft()

        # build subarray
        if token == "(":
            sublists.append(self.createSublistsHelper(tokens, list()))
            # recurse in case there are multiple sublists on this "level"
            return self.createSublistsHelper(tokens, sublists)
        if token == ")":
            # sublist is finished
            return sublists
        else:
            # append tokens to the sublist
            sublists.append(token)
            return self.createSublistsHelper(tokens, sublists)


if __name__ == "__main__":
    p = Parser()
    s = "(display (eq? 5 a))"
    print s
    tokens = p.tokenizeInput(s)
    print p.createSublists(tokens)


