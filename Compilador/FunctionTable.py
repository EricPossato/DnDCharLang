class FunctionTable:

    functions = {}
    
    def getFunction(name):
        return FunctionTable.functions[name]
    
    def setFunction(name, function):
        if name in FunctionTable.functions:
            raise Exception(f"Function {name} already exists")
        FunctionTable.functions[name] = function
    
    def functionExists(name):
        return name in FunctionTable.functions