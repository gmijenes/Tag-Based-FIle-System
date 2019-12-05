import socket
import Node
import Client 
from os import remove


class File:
    def __init__(self, name, path, id):
        self.Name = name
        self.Path = path
        self.ID = id
        self.Tags = []

def FindFile(fileID):
    for x in files:
        if files[x].ID == fileID:
            return True, files[x]
    return False, File("","",0)

def openTag(client, datos):
    tokens = datos.split()
    tags = tokens[1].split("/")
    

def openFile(client, datos):
    tokens = datos.split()
    ##localizando el file:
        ##si esta en este nodo
    findFile = FindFile(tokens[1])
    if (findFile[0]):
        myFile = findFile[1] 
        file = open(myFile.Name, "rb")
        ##e.o.c.
    else:
        me = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        me.connect((Node.Suc.ipServer, Node.Suc.puertoServidor))
        Client.openFile(me, datos)
        file = open(tokens[1], "rb")
        me.close()
    ##ya localice el file, falta mandarlo:
    content = file.read(1024)

    while content:
        client.send(content)
        content = file.read(1024)

    file.close()

    ##si el file no pertenece a este nodo, entonces debo eliminarlo

def addTag(client, datos):
    #concurrency
    tokens = datos.split()
    ##localizando el file:
        ##si esta en este nodo
    findFile = FindFile(tokens[1])
    if (findFile[0]):
        myFile = findFile[1] 
        myFile.Tags.append(tokens[2])
        ##e.o.c.
    else:
        me = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        me.connect((Node.Suc.ipServer, Node.Suc.puertoServidor))
        Client.addTag(me, datos)      
        me.close()
    print("end")
    #endconcurrency

def deleteTag(client, datos):
    #concurrency
    tokens = datos.split()
    ##localizando el file:
        ##si esta en este nodo
    findFile = FindFile(tokens[1])
    if (findFile[0]):
        myFile = findFile[1] 
        myFile.Tags.remove(tokens[2])
        ##e.o.c.
    else:
        me = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        me.connect((Node.Suc.ipServer, Node.Suc.puertoServidor))
        Client.deleteTag(me, datos)      
        me.close()
    print("end")

def addFile(client, datos):  
    tokens = datos.split()  
    file = open(tokens[1], "wb")
    input_data = client.recv(1024)
    n = 0
    while (input_data):
        file.write(input_data)
        input_data = client.recv(1024) 
    
    h = str(hash(file))
    print(h)
    files[h] = File(tokens[1], tokens[1], h)
    files[h].Tags.append('e')
    print("Received")
    file.close()

def deleteFile(client, datos):
    tokens = datos.split()
    ##localizando el file:
        ##si esta en este nodo
    findFile = FindFile(tokens[1])
    if (findFile[0]):
        myFile = findFile[1] 
        remove(myFile.Path)
        del files[myFile.ID]
        ##e.o.c.
    else:
        me = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        me.connect((Node.Suc.ipServer, Node.Suc.puertoServidor))
        Client.deleteTag(me, datos)      
        me.close()
    print("end")

def parse(line):
    tokens = line.split()
    return tokens

def initializeInstructions():
    instructions["openFile"] = openFile
    instructions["addTag"] = addTag
    instructions["addFile"] = addFile
    instructions["deleteTag"] = deleteTag
    instructions["deleteFile"] = deleteFile
    instructions["print"] = print



files = {}
instructions = {}
initializeInstructions()



ip = "0.0.0.0"
puerto = 8003
dataConection = (ip,puerto)
conexionesMaximas = 5
socketServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socketServer.bind(dataConection)

while True:
    
    socketServer.listen(conexionesMaximas)

    client, direction = socketServer.accept()
    print("tengo un cliente")
    datos = client.recv(1024)
    _datos = str(datos)
    _datos = _datos[2:len(_datos) - 1]

    print(str(_datos))

    tokens = (str(_datos)).split()
    #try:
    instructions[tokens[0]](client, str(_datos))
        #msgrecv= "recibido " + datos.decode()
        #client.sendall(msgrecv.encode())
    #except:
    #    print("error")
    #    pass
    
    client.close()

    
print("cerre la conexion")
socketServer.close()












myfile1 = File("a","a",1)
myfile2 = File("b","b",2)
files.append(myfile1)
files.append(myfile2)

deleteFile(1)

for x in files:
    print(x.Name)





