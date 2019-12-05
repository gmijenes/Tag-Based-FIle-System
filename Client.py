import socket

instructions = {}

def openFile(s, msg):
    tokens = msg.split()
    #tokens = openFile id
    s.send(msg.encode())
    file = open(tokens[1], "wb")
    input_data = s.recv(1024)
    while input_data:
        file.write(input_data)
        input_data = s.recv(1024)
    print("Received")
    file.close()

def openTag(tag):
    
    pass

def addTag(s, msg):
    s.send(msg.encode())

def addFile(s, msg):
    s.send(msg.encode())
    tokens = msg.split()
    #tokens = addFile, _path, _id
    file = open(tokens[1],"rb")
    content = file.read(1024)
    
    while content:
        s.send(content)
        content = file.read(1024)
    #try:
    #    s.send(chr(0))
    #except TypeError:
    #    s.send(bytes(chr(0), "utf-8"))
    #s.send(bytes('end'))
    file.close()
    print("The file has been send")


def deleteTag(s, msg):
    s.send(msg.encode())

def deleteFile(s, msg):
    s.send(msg.encode())

def initializeInstructions():
    instructions["openFile"] = openFile
    instructions["addTag"] = addTag
    instructions['addFile'] = addFile
    instructions["deleteTag"] = deleteTag
    instructions["deleteFile"] = deleteFile
    instructions["openTag"] = openTag
    instructions["print"] = print


#initializeInstructions()
#ipServer = "127.0.0.1"
#puertoServidor = 8001

#while True:
#    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#    client.connect((ipServer, puertoServidor))
#    print("me conecte al server")

#    msg = input("> ") 
#    print(msg)
#    tokens = msg.split()

#    try:
#        instructions[tokens[0]](client, msg)
#    except:
#        print("--There has been a syntax error--")


    #client.send(bytes(msg.encode()))
    #resp = client.recv(4096)
    #print(resp.decode())
    #if(resp.decode() == "exit"):
    #    break
    
    #client.close()
    #print("cerre la conexion")
