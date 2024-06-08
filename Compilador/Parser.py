#Parser class
#Atributes: tokenizer (Tokenizer)
#Methods: parseExpression(), run(code : string)

from Tokenizer import Tokenizer
from Nodes import Node, BinOp, UnOp, IntVal, NoOp, Block, Assignment, Identifier, PrintNode, IfNode, WhileNode, RollNode, StrVal, VarDec, FuncDec, FuncCall, ReturnNode, TypeNode
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
        elif Parser.tokenizer_used.next.type == "roll":
            Parser.tokenizer_used.selectNext()
            if Parser.tokenizer_used.next.type != "OPENPAREN":
                raise Exception(f"Unexpected token {Parser.tokenizer_used.next.type} at position {Parser.tokenizer_used.position}")
            Parser.tokenizer_used.selectNext()
            result = Parser.parseRelExpression()
            if Parser.tokenizer_used.next.type != "CLOSEPAREN":
                raise Exception(f"Unexpected token {Parser.tokenizer_used.next.type} at position {Parser.tokenizer_used.position}")
            Parser.tokenizer_used.selectNext()
            return RollNode(None, children=[result])
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
        
        elif Parser.tokenizer_used.next.type == "turns":
            Parser.tokenizer_used.selectNext()
            result = Parser.parseRelExpression()
            if Parser.tokenizer_used.next.type != "action":
                raise Exception(f"Unexpected token {Parser.tokenizer_used.next.type} at position {Parser.tokenizer_used.position}")
            Parser.tokenizer_used.selectNext()
            if Parser.tokenizer_used.next.type != "NEWLINE":
                raise Exception(f"Unexpected token {Parser.tokenizer_used.next.type} at position {Parser.tokenizer_used.position}")
            Parser.tokenizer_used.selectNext()
            statements = []
            while Parser.tokenizer_used.next.type != "rest":
                statements.append(Parser.parseStatement())
            Parser.tokenizer_used.selectNext()
            return WhileNode(value=None, children=[result, Block(None, statements)])

        elif Parser.tokenizer_used.next.type == "stat" or Parser.tokenizer_used.next.type == "narration":
            variableType = Parser.tokenizer_used.next.type
            typeNode = TypeNode(variableType, [])
            Parser.tokenizer_used.selectNext()
            if Parser.tokenizer_used.next.type != "ID":
                raise Exception(f"Unexpected token {Parser.tokenizer_used.next.type} at position {Parser.tokenizer_used.position}")
            identifier = Identifier(Parser.tokenizer_used.next.value, [])
            Parser.tokenizer_used.selectNext()
            if Parser.tokenizer_used.next.type == "=":
                Parser.tokenizer_used.selectNext()
                val = Parser.parseRelExpression()
                if variableType == "stat" and type(val) != IntVal:
                    raise Exception(f"Invalid type {type(val)} in VarDec")
                elif variableType == "narration" and type(val) != StrVal:
                    raise Exception(f"Invalid type {type(val)} in VarDec")
                return VarDec(None, [identifier, typeNode, val])
            return VarDec(None, [identifier, typeNode])
        elif Parser.tokenizer_used.next.type == "check":
            Parser.tokenizer_used.selectNext()
            result = Parser.parseRelExpression()
            if Parser.tokenizer_used.next.type != "NEWLINE":
                raise Exception(f"Unexpected token {Parser.tokenizer_used.next.type} at position {Parser.tokenizer_used.position}")
            Parser.tokenizer_used.selectNext()
            if Parser.tokenizer_used.next.type != "success":
                raise Exception(f"Unexpected token {Parser.tokenizer_used.next.type} at position {Parser.tokenizer_used.position}")
            Parser.tokenizer_used.selectNext()
            statements = []
            while Parser.tokenizer_used.next.type != "consequence":
                statements.append(Parser.parseStatement())
            Parser.tokenizer_used.selectNext()
            success_block = Block(None, statements)
            consequence_statements = []
            while Parser.tokenizer_used.next.type != "rest":
                consequence_statements.append(Parser.parseStatement())
            Parser.tokenizer_used.selectNext()
            if Parser.tokenizer_used.next.type != "NEWLINE" and Parser.tokenizer_used.next.type != "EOF":
                raise Exception(f"Unexpected token {Parser.tokenizer_used.next.type} at position {Parser.tokenizer_used.position}")
            consequence_block = Block(None, consequence_statements)

            check_node = IfNode(None, [result, success_block, consequence_block])
            return check_node


            

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
    

