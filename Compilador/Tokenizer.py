#Tokenizer class
#Atributes: source (string), position (int), next (Token)
#Methods: selectNext() 

from Token import Token
from PrePro import PrePro

reserved = ["print", "if","else","while","do","then","end","and","or","not","read", "local","function","return"]

class Tokenizer:
    next = None
    def __init__(self, source):
        self.source = PrePro.filter(source)
        self.position = 0

    def selectNext(self) -> None:
        if self.position >= len(self.source):
            self.next = Token("EOF", None)
        else:
            while self.source[self.position] == " " or self.source[self.position] == "\t":
                if self.position == len(self.source) - 1:
                    self.next = Token("EOF", None)
                    return
                self.position += 1
            
            if self.source[self.position] == "+":
                self.position += 1
                self.next = Token("PLUS", None)
            elif self.source[self.position] == "-":
                self.position += 1
                self.next = Token("MINUS", None)
            elif self.source[self.position] == "*":
                self.position += 1
                self.next = Token("MULTIPLY", None)
            elif self.source[self.position] == "/":
                self.position += 1
                self.next = Token("DIVIDE", None)
            elif self.source[self.position] == "(":
                self.position += 1
                self.next = Token("OPENPAREN", None)
            elif self.source[self.position] == ")":
                self.position += 1
                self.next = Token("CLOSEPAREN", None)
            elif self.source[self.position].isdigit():
                start = self.position
                while self.position < len(self.source) and self.source[self.position].isdigit():
                    self.position += 1
                self.next = Token("NUMBER", int(self.source[start:self.position]))
            elif self.source[self.position] == "\n":
                self.next = Token("NEWLINE", None)
                self.position += 1
            elif self.source[self.position] == "=":
                if self.source[self.position + 1] == "=":
                    self.next = Token("==", None)
                    self.position += 2
                else:
                    self.next = Token("=", None)
                    self.position += 1
            elif str.isalpha(self.source[self.position]):
                start = self.position
                while self.position < len(self.source) and (self.source[self.position].isalnum() or self.source[self.position] == "_"):
                    self.position += 1
                self.next = Token("ID", self.source[start:self.position])
                if self.next.value in reserved:
                    self.next = Token(self.next.value, None)
            elif self.source[self.position] == "<":
                self.next = Token("<", None)
                self.position += 1
            elif self.source[self.position] == ">":
                self.next = Token(">", None)
                self.position += 1
            elif self.source[self.position] == ".":
                if self.source[self.position + 1] == ".":
                    self.next = Token("CONCAT", None)
                    self.position += 2
                else:
                    raise Exception(f"Unexpected token {self.source[self.position]}")
            elif self.source[self.position] == "\"":
                start = self.position + 1
                self.position += 1
                while self.source[self.position] != "\"":
                    self.position += 1
                    if self.position == len(self.source):
                        raise Exception("Unexpected EOF")
                self.next = Token("STRING", self.source[start:self.position])
                self.position += 1
            elif self.source[self.position] == ",":
                self.next = Token("COMMA", None)
                self.position += 1
            else:
                raise Exception(f"Unexpected token {self.source[self.position]}")


    