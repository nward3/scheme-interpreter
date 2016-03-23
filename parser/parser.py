#!/usr/bin/python
import collections
import math
import operator as op

class Parser:

    # uses Parser class methods to return tokenized sublists
    # input: code as a string
    def parse(self, code):
        if self.hasBalancedParens(code):
            tokens = self.tokenizeInput(code)
            tokensSublists = self.createSublists(tokens)

            return tokensSublists

    # input: input file/code
    # output: array of tokens of code
    def tokenizeInput(self, code):
        # add whitespace around parens and single quote so they can be split correctly
        code = code.replace("(", " ( ").replace(")", " ) ").replace("'", " ' ")
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
                if isinstance(x, list):
                    # previous element was a single quote
                    newSublists.append(["'", x])
                    isQuote = False
                else:
                    raise ParseError("Improper use of single quote. Single quote should precede a list: " + "'" + str(x))
            elif isinstance(x, list):
                newSublists.append(self.quotify(x))
            else:
                newSublists.append(x)

        if isQuote == True:
            raise ParseError("Improper use of single quote. Single quote should precede a list")

        return newSublists

    # convert nested array structure back to parenthesis
    def convertToParens(self, sublists):
        if not isinstance(sublists, list):
            return sublists
        elif len(sublists) == 0:
            # edge case
            return '()'

        parenStr = '('
        for x in sublists:
            if isinstance(x, list):
                parenStr += self.convertToParens(x)
            else:
                parenStr += str(x) + ' '

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

    # returns True if string has balanced parens
    # raises ParseError if string's parens are not balanced 
    def hasBalancedParens(self, inputStr):
        # increase match count upon '('
        # decrease match count upon ')'
        matchCount = 0
        charCount = 0

        for char in inputStr:
            charCount += 1

            if char == '(':
                matchCount += 1
            elif char == ')':
                matchCount -= 1

            if matchCount < 0:
                raise ParseError("Invalid ) at position " + str(charCount) + " in code: " + inputStr)

        if matchCount == 0:
            return True
        else:
            raise ParseError("Parens are not balanced in code: " + inputStr)


class ParseError(Exception):
    pass
