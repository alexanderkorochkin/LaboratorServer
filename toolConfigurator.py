class Var:
    def __init__(self, data_var, opcua_var):
        self.Data = data_var
        self.Var = opcua_var

    def getVar(self):
        return self.Var

    def getData(self):
        return self.Data

    def Print(self):
        _index = self.Data.GetIndex()
        _name = self.Data.GetName()
        _value = self.Var.get_value()
        return [_index, _name, _value]


class VarData:
    isExecuted = False
    index = 0
    port = 0
    name = "NONE"
    multiplier = 1

    def __init__(self, index, port, name, multiplier=1):
        self.isExecuted = True
        self.index = index
        self.port = port
        self.name = name
        self.multiplier = multiplier

    def GetName(self):
        if self.isExecuted:
            return self.name
        else:
            return -1

    def GetPort(self):
        if self.isExecuted:
            return self.port
        else:
            return -1

    def GetIndex(self):
        if self.isExecuted:
            return self.index
        else:
            return -1

    def GetMultiplier(self):
        if self.isExecuted:
            return self.multiplier
        else:
            return -1

    def SetName(self, name):
        self.name = name

    def SetPort(self, port):
        self.port = port

    def SetIndex(self, index):
        self.index = index

    def SetMultiplier(self, multiplier):
        self.multiplier = multiplier


def Configure(path):
    arr = []
    file = open(path, "r")
    for line in file:
        index, port, name, *multiplier = line.split("\t", 4)
        arr.append(VarData(index, port, name, multiplier[0]))
    file.close()
    return arr
