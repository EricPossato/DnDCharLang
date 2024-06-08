from abc import ABC, abstractmethod
from SymbolTable import SymbolTable
from FunctionTable import FunctionTable
class Node(ABC):
    
    def __init__(self, value, children):
        self.value = value
        self.children = children
    
    @abstractmethod
    def evaluate(self,symbol_table):
        pass


class BinOp(Node):
    
    def evaluate(self, symbol_table):
        if self.value == "+":
            return (self.children[0].evaluate(symbol_table)[0] + self.children[1].evaluate(symbol_table)[0],"INT")
        elif self.value == "-":
            return (self.children[0].evaluate(symbol_table)[0] - self.children[1].evaluate(symbol_table)[0],"INT")
        elif self.value == "*":
            return (self.children[0].evaluate(symbol_table)[0] * self.children[1].evaluate(symbol_table)[0],"INT")
        elif self.value == "/":
            return (self.children[0].evaluate(symbol_table)[0] // self.children[1].evaluate(symbol_table)[0],"INT")
        elif self.value == "DC":
            return (self.children[0].evaluate(symbol_table)[0] >= self.children[1].evaluate(symbol_table)[0],"INT")
        else:
            raise Exception(f"Unexpected token {self.value}") 
        
class UnOp(Node):
    
    def evaluate(self, symbol_table):
        if self.value == "+":
            return (self.children[0].evaluate(symbol_table)[0], "INT")
        elif self.value == "-":
            return (-self.children[0].evaluate(symbol_table)[0], "INT")
        elif self.value == "not":
            return (not self.children[0].evaluate(symbol_table)[0], "INT")
        else:
            raise Exception(f"Unexpected token {self.value} in UnOp.evaluate()")

class IntVal(Node):

    def evaluate(self, symbol_table):
        return (int(self.value), "INT")
    
class NoOp(Node):
    
    def evaluate(self, symbol_table):
        return None
    

class Block(Node):

    def evaluate(self,symbol_table):
        for child in self.children:
            if type(child) == ReturnNode:
                return child.evaluate(symbol_table)
            child.evaluate(symbol_table)


class Identifier(Node):

    def evaluate(self, symbolTable):
        return symbolTable.getValue(self.value)


class Assignment(Node):

    def evaluate(self,symbol_table):
        val = self.children[1].evaluate(symbol_table)
        symbol_table.setValue(self.children[0].value,val)

class PrintNode(Node):
    
    def evaluate(self,symbol_table):
        target = self.children[0].evaluate(symbol_table)
        if target[1] == "INT":
            print(int(target[0]))
        elif target[1] == "STRING":
            print(target[0])
        else:
            raise Exception(f"Invalid type {target[1]} in PrintNode.evaluate()")

class IfNode(Node):
    
    def evaluate(self,symbol_table):
        if self.children[0].evaluate(symbol_table)[0]:
            self.children[1].evaluate(symbol_table)
        elif len(self.children) == 3:
            self.children[2].evaluate(symbol_table)

class WhileNode(Node):
        
        def evaluate(self,symbol_table):
            while self.children[0].evaluate(symbol_table)[0]:
                self.children[1].evaluate(symbol_table)

class ReadNode(Node):
    
    def evaluate(self,symbol_table):
        val = int(input())
        return (val,"INT")
        

class StrVal(Node):

    def evaluate(self, symbol_table):
        return (str(self.value), "STRING")
    
class VarDec(Node):

    def evaluate(self,symbol_table):
        variableType = self.children[1].value
        symbol_table.createVariable(self.children[0].value, variableType)
        if len(self.children) == 3:
            var = self.children[2].evaluate(symbol_table)
            symbol_table.setValue(self.children[0].value, var)

class FuncDec(Node):

    def evaluate(self,symbol_table):
        name = self.children[0].value
        if FunctionTable.functionExists(name):
            raise Exception(f"Function {name} already exists")
        FunctionTable.setFunction(name, self)

class FuncCall(Node):

    def evaluate(self,symbol_table):
        function = FunctionTable.getFunction(self.value)
        if function is None:
            raise Exception(f"Function {self.value} not found")
        args = function.children[1:-1]
        if len(args) != len(self.children):
            raise Exception(f"Function {self.value} expected {len(args)} arguments, got {len(self.children)}")
        new_symbol_table = SymbolTable()
        for i in range(len(args)):
            new_symbol_table.createVariable(args[i].value)
            new_symbol_table.setValue(args[i].value, self.children[i].evaluate(symbol_table))
        
        return function.children[-1].evaluate(new_symbol_table)
    
class ReturnNode(Node):
    
        def evaluate(self,symbol_table):
            return self.children[0].evaluate(symbol_table)
        
class TypeNode(Node):
    
    def evaluate(self,symbol_table):
        return self.value