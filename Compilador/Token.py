#Token class 
#Atributes : type (string), value (int)


class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __str__(self):
        return f"Type : {self.type}, Value : {self.value}"
    
    
    