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

    def createSublists(self, tokens):
        return self.createSublistsHelper(collections.deque(tokens), [])

    def createSublistsHelper(self, tokens, sublists):
        print tokens
	
	# maps potential scheme variables to their values
	def tokenMapper():
		mapper = dict()
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
			'null?': lambda x: x == [],
		})

		return mapper

	# determines the type of a token
	def determineTokenType(token):
		try:
			return int(token)
		except ValueError:
			try:
				return float(token)
			except:
				return str(token)

if __name__ == "__main__":
    p = Parser()
    s = "(display (eq? 5 a))"
    print s
    tokens = p.tokenizeInput(s)
    p.createSublists(tokens)

