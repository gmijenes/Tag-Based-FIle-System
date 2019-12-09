import socket
import Node
import Client 
from os import remove
import threading


class File:
    def __init__(self, name, path, id, fromPrev):
        self.Name = name
        self.Path = path
        self.ID = id
        self.Tags = []
        self.FromPrev = fromPrev

def FindFile(fileID):
    for x in files:
        if files[x].ID == fileID:
            return True, files[x]
    return False, File("","",0)

def openTag(client, datos):
    #inicializando estructuras y datos
    mFiles = []
    mTags = []
    tokens = datos.split()
    tags = tokens[1].split("/")
    
    #creando las listas
    for x in files:
        match = 1
        for t in tags:
            if t not in files[x].Tags:
                match = 0
        if match:
            if len(files[x].Tags) == len(tags):
                mFiles.append(files[x])
            else:
                for t in files[x].Tags:
                    if t not in tags:
                        mTags.append(t)
                        
    hostName = socket.gethostname()
    #si soy el nodo inicial => engancho mi ip y mi puerto
    if len(tokens) == 2:
        hostName = socket.gethostname()
        datos = datos + ' ' + socket.gethostbyname(hostName) + ' ' + str(node.Adress.puertoServidor)
        tokens = datos.split()
        
        me = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        me.connect((node.Suc.ipServer, node.Suc.puertoServidor))
        Client.openTag(me, datos)
        ftags = open("tags", "a")
        for x in mTags:
            ftags.write(x + '\n')
        ftags.close()
        ffiles = open("files", "a")
        for x in mFiles:
            ffiles.write(str(x.ID) + '  ' + files[x.ID].Path + '\n')
        ffiles.close()
    
        me.close()
    tokens = datos.split()
    #consultando que el siguiente no sea el nodo inicial,
    #y en ese caso, pidiendo informacion al siguiente nodo
    if (tokens[2] != socket.gethostbyname(hostName) or tokens[3] != str(node.Adress.puertoServidor)):
        me = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        me.connect((node.Suc.ipServer, node.Suc.puertoServidor))
        Client.openTag(me, datos)
        ftags = open("tags", "a")
        for x in mTags:
            ftags.write(x)
        ftags.close()
        ffiles = open("files", "a")
        for x in mFiles:
            ffiles.write(str(x.ID) + '  ' + files[x.ID].Path + '\n')
        ffiles.close()
    
        me.close()

        #ftags = open("tags", "a")
        #for x in mTags:
        #    ftags.write(x)
        #ftags.close()
        #ffiles = open("files", "a")
        #for x in mFiles:
        #    ffiles.write(str(x.ID) + '  ' + files[x.ID].Path + '\n')
        #ffiles.close()

    else:
        ftags = open("tags", "w")
        for x in mTags:
            ftags.write(x + '\n') 
        ftags.close()
        ffiles = open("files", "w")
        for x in mFiles:
            ffiles.write(str(x.ID) + x.Path)
        ffiles.close()

    #mandando los files
    ffiles = open("files", "rb") 
    input_data = ffiles.read(1024)
    while input_data:
        client.send(input_data)
        input_data = ffiles.read(1024)
    ffiles.close()

    ftags = open("tags", "rb")
    #mandando los tags
    input_data = ftags.read(1024)
    while input_data:
        client.send(input_data)
        input_data = ftags.read(1024)
    ftags.close() 

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
        me.connect((node.Suc.ipServer, node.Suc.puertoServidor))
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
        me.connect((node.Suc.ipServer, node.Suc.puertoServidor))
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
        me.connect((node.Suc.ipServer, node.Suc.puertoServidor))
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
    files[h] = File(tokens[1], tokens[1], h, False)
    files[h].Tags.append('e')
    print("Received")

    me = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    me.connect((node.Suc.ipServer, node.Suc.puertoServidor))
    datos = 'addFileKey' + ' ' + tokens[1] + ' '+  h
    print(datos)
    Client.addFileKey(me, datos, True)      
    me.close()

    
    file.close()

def addFileKey(client, datos):
    tokens = datos.split()
    file = open(tokens[1], "wb")
    input_data = client.recv(1024)
    n = 0
    while(input_data):
        file.write(input_data)
        input_data = client.recv(1024)
        
    h = tokens[2]
    print(h)
    files[h] = File(tokens[1], tokens[1], h, True)
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
        me.connect((node.Suc.ipServer, node.Suc.puertoServidor))
        Client.deleteTag(me, datos)      
        me.close()
    print("end")

def parse(line):
    tokens = line.split()
    return tokens

def update(client, datos):    
    client.send((node.Prev.ipServer + ':' + str(node.Prev.puertoServidor)).encode())

    suc_str = client.recv(1024)
    node.Suc = Node.Conection(suc_str.decode())

    for x in files:
        client.send("newFile")
        msg = 'addFileKey' + ' ' + files[x].path + ' ' + files[x].ID
        addFileKey(client, msg)
        client.recv(1024)

def gettinIn(prev_str, suc_str):
    
        

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((node.Prev.ipServer, node.Prev.puertoServidor))
    
    sucServer = client.recv(1024)

    client.send(("update").encode())

    pprev_str = client.recv(1024)  
    node.Pprev = Node.Conection(pprev_str.decode())

    hostName = socket.gethostname()
    hostAddr = socket.gethostbyname(hostName)
    client.send((hostAddr + ':'  + str(puerto)).encode())

    msg = client.recv(1024)
    while msg:
        if msg == 'newFile':
            Client.addFileKey(client, msg, False)
            client.send(("ok").encode())
            msg = client.recv(1024)

def initializeInstructions():
    instructions["openFile"] = openFile
    instructions["openTag"] = openTag
    instructions["addTag"] = addTag
    instructions["addFile"] = addFile
    instructions["deleteTag"] = deleteTag
    instructions["deleteFile"] = deleteFile
    instructions["print"] = print
    instructions["addFileKey"] = addFileKey
    instructions["update"] = update

def worker(*args):
    client = args[0]
    direction = args[1]
    print("tengo un cliente")
    client.send((node.Suc.ipServer +  ':' + str(node.Suc.puertoServidor)).encode())
    datos = client.recv(1024)
    _datos = str(datos)
    _datos = _datos[2:len(_datos) - 1]

    print(str(_datos))

    tokens = (str(_datos)).split()
    try:
        instructions[tokens[0]](client, str(_datos))
        #msgrecv= "recibido " + datos.decode()
        #client.sendall(msgrecv.encode())
    except:
        print("error")
    #    pass
    client.close()



    # recibir todos los elementos del hijo

files = {}
instructions = {}
initializeInstructions()

ip = "0.0.0.0"
puerto = 8081

pprev = Node.Conection('10.1.1.1:8000')
prev = Node.Conection('10.1.1.1:8000')
suc = Node.Conection('127.0.0.1:8082')
add = Node.Conection(ip+':'+str(puerto))
node = Node.Node(prev, suc, prev, add)

print("Introduzca IP:puerto del nodo sucesor")
suc_str = input(">")

print("Introduzca IP:puerto del nodo antecesor")
prev_str = input(">")


node.Suc = Node.Conection(suc_str)
node.Prev = Node.Conection(prev_str)

try:
    
    gettinIn( prev_str, suc_str)

except:
    print("No hay red existente, se iniciará una nueva red.")


dataConection = (ip,puerto)
conexionesMaximas = 5
socketServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socketServer.bind(dataConection)


print( ip + ' ' + str(puerto))

while True:
    
    socketServer.listen(conexionesMaximas)
    client, direction = socketServer.accept()
    threading.Thread(target=worker, args=(client, direction)).start()
    

    
print("cerre la conexion")
socketServer.close()












myfile1 = File("a","a",1)
myfile2 = File("b","b",2)
files.append(myfile1)
files.append(myfile2)

deleteFile(1)

for x in files:
    print(x.Name)





