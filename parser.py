#!/usr/bin/python
import collections
import math
import operator as op

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
        # call quotify to handle ' tokens, which indicate to handle list literally
        return self.quotify(sublists[0])

    # tokens is a deque for optimized pop(0) operation
    # sublists is a list
    def createSublistsHelper(self, tokens, sublists):
        # base case
        if len(tokens) == 0:
            # no tokens left
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
            sublists.append(self.determineTokenType(token))
            return self.createSublistsHelper(tokens, sublists)

    # look for ' tokens: replace ' and nextToken with a single list: [', nextToken]
    def quotify(self, sublists):
        newSublists = []
        isQuote = False
        for x in sublists:
            if x == "'":
                isQuote = True
            elif isQuote == True:
                # previous element was a single quote
                newSublists.append(["'", x])
                isQuote = False
            elif isinstance(x, list):
                newSublists.append(self.quotify(x))
            else:
                newSublists.append(x)

        if isQuote == True:
            raise Exception("Improper use of single quote")

        return newSublists

    # convert nested array structure back to parenthesis
    def convertToParens(self, sublists):
        if not isinstance(sublists, list):
            return sublists

        parenStr = '('
        for x in sublists:
            if isinstance(x, list):
                parenStr = parenStr + self.convertToParens(x)
            else:
                parenStr = parenStr + str(x) + ' '

        # add ending paren, and remove the space that preceeds it
        parenStr = parenStr[0:-1] + ')'

        return parenStr

    # determines the type of a token
    def determineTokenType(self, token):
        try:
            return int(token)
        except ValueError:
            try:
                return float(token)
            except:
                return str(token)

