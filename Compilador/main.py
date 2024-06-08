import sys
from Parser import Parser
from SymbolTable import SymbolTable
from FunctionTable import FunctionTable

with open(sys.argv[1], "r") as file:
    code = file.read()

symbol_table = SymbolTable()
Parser.run(code = code).evaluate(symbol_table)