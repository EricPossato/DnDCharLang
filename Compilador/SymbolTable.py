class SymbolTable():
    
    def __init__(self):
        self.symbols = {}
        
    def getValue(self, key):
        return self.symbols[key]
    
    def setValue(self, key, var):
        if key not in self.symbols:
            raise Exception(f"Variable {key} not found")
        self.symbols[key] = var

    def createVariable(self, key):
        if key in self.symbols:
            raise Exception(f"Variable {key} already exists")
        self.symbols[key] = (None, None)