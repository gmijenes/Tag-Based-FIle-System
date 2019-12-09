class Node:
    def __init__(self,prev, pprev, suc, add):
        self.Prev = prev
        self.Pprev = pprev
        
        self.Suc = suc
        
        self.Adress = add

class Conection:
    def __init__(self, connection):
        tokens = connection.split(':')
        self.ipServer = tokens[0]
        self.puertoServidor = int(tokens[1])
