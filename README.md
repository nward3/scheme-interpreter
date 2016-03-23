# Scheme Interpreter

This basic Scheme interpreter is a python-based program that evaluates many basic
Scheme expressions by using the concepts of context-free grammars and building up
an abstract syntax tree that recognizes a subset of the Scheme language.


## Running

This Scheme interpreter is run from the command line by using the Python interpreter
with python version 2.7.10. The interpreter utilizes the collections, math, and operator
modules. The main program is run on the command line using a valid Scheme file specified
by the user as input. The main program is accompanied by files containing the Parser and
Interpreter classes used for the two main parts of the main program.


## Using

The interpreter can be used by running the command: python main.py <filename>
where <filename> represents the valid Scheme file specified by the user and used as input
to the interpreter. Once the program is started, it will run the input file through the
parser and then the interpreter. After these two steps are completed, the evaluated Scheme
expression is output to the user.

Example scheme code has been included in the examples folder, in files 1-6. The example code can be used as follows: python main.py examples/[1-6]
