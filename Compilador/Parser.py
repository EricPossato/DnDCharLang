#Parser class
#Atributes: tokenizer (Tokenizer)
#Methods: parseExpression(), run(code : string)

from Tokenizer import Tokenizer
from Nodes import Node, BinOp, UnOp, IntVal, NoOp, Block, Assignment, Identifier, PrintNode, IfNode, WhileNode, ReadNode, StrVal, VarDec, FuncDec, FuncCall, ReturnNode

class Parser:

    tokenizer_used = Tokenizer

    def __init__(self):
        pass
  
    @staticmethod
    def parseTerm() -> int:
        result = Parser.parseFactor()

        while Parser.tokenizer_used.next.type == "MULTIPLY" or Parser.tokenizer_used.next.type == "DIVIDE":

            if Parser.tokenizer_used.next.type == "MULTIPLY":
                Parser.tokenizer_used.selectNext()
                result = BinOp("*", [result, Parser.parseFactor()])
            
            elif Parser.tokenizer_used.next.type == "DIVIDE":
                Parser.tokenizer_used.selectNext()
                result = BinOp("/", [result, Parser.parseFactor()])
        return result

    @staticmethod
    def parseExpression() -> int:
        result = Parser.parseTerm()
        while Parser.tokenizer_used.next.type == "PLUS" or Parser.tokenizer_used.next.type == "MINUS":
            if Parser.tokenizer_used.next.type == "PLUS":
                Parser.tokenizer_used.selectNext()
                result = BinOp("+", [result, Parser.parseTerm()])
            elif Parser.tokenizer_used.next.type == "MINUS":
                Parser.tokenizer_used.selectNext()
                result = BinOp("-", [result, Parser.parseTerm()])
        return result
    
    @staticmethod
    def parseFactor() -> int:
        if Parser.tokenizer_used.next.type == "NUMBER":
            result = IntVal(Parser.tokenizer_used.next.value, [])
            Parser.tokenizer_used.selectNext()
            return result
        elif Parser.tokenizer_used.next.type == "PLUS":
            Parser.tokenizer_used.selectNext()
            return UnOp("+", [Parser.parseFactor()])
        elif Parser.tokenizer_used.next.type == "MINUS":
            Parser.tokenizer_used.selectNext()
            return UnOp("-", [Parser.parseFactor()])
        elif Parser.tokenizer_used.next.type == "not":
            Parser.tokenizer_used.selectNext()
            return UnOp("not", [Parser.parseFactor()])
        elif Parser.tokenizer_used.next.type == "OPENPAREN":
            Parser.tokenizer_used.selectNext()
            result = Parser.parseRelExpression()
            if Parser.tokenizer_used.next.type != "CLOSEPAREN":
                raise Exception(f"Unexpected token {Parser.tokenizer_used.next.type} at position {Parser.tokenizer_used.position}")
            Parser.tokenizer_used.selectNext()
            return result
        elif Parser.tokenizer_used.next.type == "ID":
            result = Identifier(Parser.tokenizer_used.next.value, [])
            identifier = Parser.tokenizer_used.next.value
            Parser.tokenizer_used.selectNext()
            if Parser.tokenizer_used.next.type == "OPENPAREN":
                Parser.tokenizer_used.selectNext()
                parameters = []
                if Parser.tokenizer_used.next.type != "CLOSEPAREN":
                    parameters.append(Parser.parseRelExpression())
                    while Parser.tokenizer_used.next.type == "COMMA":
                        Parser.tokenizer_used.selectNext()
                        parameters.append(Parser.parseRelExpression())
                if Parser.tokenizer_used.next.type != "CLOSEPAREN":
                    raise Exception(f"Unexpected token {Parser.tokenizer_used.next.type} at position {Parser.tokenizer_used.position}")
                Parser.tokenizer_used.selectNext()
                result = FuncCall(identifier, parameters)
            return result
        elif Parser.tokenizer_used.next.type == "read":
            Parser.tokenizer_used.selectNext()
            if Parser.tokenizer_used.next.type != "OPENPAREN":
                raise Exception(f"Unexpected token {Parser.tokenizer_used.next.type} at position {Parser.tokenizer_used.position}")
            Parser.tokenizer_used.selectNext()
            if Parser.tokenizer_used.next.type != "CLOSEPAREN":
                raise Exception(f"Unexpected token {Parser.tokenizer_used.next.type} at position {Parser.tokenizer_used.position}")
            Parser.tokenizer_used.selectNext()
            return ReadNode(None, [])
        elif Parser.tokenizer_used.next.type == "STRING":
            result = StrVal(Parser.tokenizer_used.next.value, [])
            Parser.tokenizer_used.selectNext()
            return result
        else:
            raise Exception(f"Unexpected token {Parser.tokenizer_used.next.type} at position {Parser.tokenizer_used.position}")

    @staticmethod
    def parseStatement():
        if Parser.tokenizer_used.next.type == "NEWLINE":
            Parser.tokenizer_used.selectNext()
            return NoOp(None, [])
        elif Parser.tokenizer_used.next.type == "ID":
            identifier = Identifier(Parser.tokenizer_used.next.value, [])
            Parser.tokenizer_used.selectNext()

            if Parser.tokenizer_used.next.type == "=":
                Parser.tokenizer_used.selectNext()
                return Assignment(value=None, children=[identifier, Parser.parseRelExpression()])
            elif Parser.tokenizer_used.next.type == "OPENPAREN":
                Parser.tokenizer_used.selectNext()
                parameters = []
                if Parser.tokenizer_used.next.type != "CLOSEPAREN":
                    parameters.append(Parser.parseRelExpression())
                    while Parser.tokenizer_used.next.type == "COMMA":
                        Parser.tokenizer_used.selectNext()
                        parameters.append(Parser.parseRelExpression())
                if Parser.tokenizer_used.next.type != "CLOSEPAREN":
                    raise Exception(f"Unexpected token {Parser.tokenizer_used.next.type} at position {Parser.tokenizer_used.position}")
                Parser.tokenizer_used.selectNext()
                return FuncCall(identifier.value, parameters)

        elif Parser.tokenizer_used.next.type == "say":
            Parser.tokenizer_used.selectNext()
            
            if Parser.tokenizer_used.next.type != "OPENPAREN":
                raise Exception(f"Unexpected token {Parser.tokenizer_used.next.type} at position {Parser.tokenizer_used.position}")
            Parser.tokenizer_used.selectNext()
            result = Parser.parseRelExpression()
            if Parser.tokenizer_used.next.type != "CLOSEPAREN":
                raise Exception(f"Unexpected token {Parser.tokenizer_used.next.type} at position {Parser.tokenizer_used.position}")
            Parser.tokenizer_used.selectNext()
            return PrintNode(value=None, children=[result])
        
        elif Parser.tokenizer_used.next.type == "while":
            Parser.tokenizer_used.selectNext()
            result = Parser.parseRelExpression()
            if Parser.tokenizer_used.next.type != "do":
                raise Exception(f"Unexpected token {Parser.tokenizer_used.next.type} at position {Parser.tokenizer_used.position}")
            Parser.tokenizer_used.selectNext()
            if Parser.tokenizer_used.next.type != "NEWLINE":
                raise Exception(f"Unexpected token {Parser.tokenizer_used.next.type} at position {Parser.tokenizer_used.position}")
            Parser.tokenizer_used.selectNext()
            statements = []
            while Parser.tokenizer_used.next.type != "end":
                statements.append(Parser.parseStatement())
            Parser.tokenizer_used.selectNext()
            return WhileNode(value=None, children=[result, Block(None, statements)])
        
        elif Parser.tokenizer_used.next.type == "if":
            Parser.tokenizer_used.selectNext()
            result = Parser.parseRelExpression()
            if Parser.tokenizer_used.next.type != "then":
                raise Exception(f"Unexpected token {Parser.tokenizer_used.next.type} at position {Parser.tokenizer_used.position}")
            Parser.tokenizer_used.selectNext()
            if Parser.tokenizer_used.next.type != "NEWLINE":
                raise Exception(f"Unexpected token {Parser.tokenizer_used.next.type} at position {Parser.tokenizer_used.position}")
            Parser.tokenizer_used.selectNext()

            statements = []
            while Parser.tokenizer_used.next.type != "end" and Parser.tokenizer_used.next.type != "else":
                statements.append(Parser.parseStatement())
            if Parser.tokenizer_used.next.type == "else":
                if_block = Block(value=None,children=statements)
                Parser.tokenizer_used.selectNext()
                if Parser.tokenizer_used.next.type != "NEWLINE":
                    raise Exception(f"Unexpected token {Parser.tokenizer_used.next.type} at position {Parser.tokenizer_used.position}")
                Parser.tokenizer_used.selectNext()

                else_statements = []
                while Parser.tokenizer_used.next.type != "end":
                    else_statements.append(Parser.parseStatement())
                Parser.tokenizer_used.selectNext()
                if Parser.tokenizer_used.next.type != "EOF" and Parser.tokenizer_used.next.type != "NEWLINE":
                    raise Exception(f"Unexpected token {Parser.tokenizer_used.next.type} at position {Parser.tokenizer_used.position}")
                else_block = Block(value=None,children=else_statements)
                if_node = IfNode(value=None,children=[result,if_block,else_block])
                return if_node
            Parser.tokenizer_used.selectNext()
            if Parser.tokenizer_used.next.type != "EOF" and Parser.tokenizer_used.next.type != "NEWLINE":
                raise Exception(f"Unexpected token {Parser.tokenizer_used.next.type} at position {Parser.tokenizer_used.position}")
            if_block = Block(value=None,children=statements)
            if_node = IfNode(value=None, children=[result,if_block])
            return if_node
        elif Parser.tokenizer_used.next.type == "local":
            Parser.tokenizer_used.selectNext()
            if Parser.tokenizer_used.next.type != "ID":
                raise Exception(f"Unexpected token {Parser.tokenizer_used.next.type} at position {Parser.tokenizer_used.position}")
            identifier = Identifier(Parser.tokenizer_used.next.value, [])
            Parser.tokenizer_used.selectNext()
            if Parser.tokenizer_used.next.type != "=":
                return VarDec(value=None, children=[identifier])
            else:
                Parser.tokenizer_used.selectNext()
                return VarDec(value=None, children=[identifier, Parser.parseRelExpression()])
        else:
            raise Exception(f"Unexpected token {Parser.tokenizer_used.next.type} at position {Parser.tokenizer_used.position}")
        
            

    @staticmethod
    def parseBlock():
        result = Block(value=None, children=[])
        while Parser.tokenizer_used.next.type != "EOF":
            result.children.append(Parser.parseStatement())
        return result
    
    @staticmethod
    def parseRelExpression():
        result = Parser.parseExpression()
        if Parser.tokenizer_used.next.type == "DC":
            Parser.tokenizer_used.selectNext()
            return BinOp("DC", [result, Parser.parseExpression()])
        else:
            return result

    @staticmethod
    def run(code):
        Parser.tokenizer_used = Tokenizer(code)
        Parser.tokenizer_used.selectNext()
        result = Parser.parseBlock()
        if Parser.tokenizer_used.next.type != "EOF":
            raise Exception(f"Unexpected token {Parser.tokenizer_used.next.type} at position {Parser.tokenizer_used.position}")
        return result
    

