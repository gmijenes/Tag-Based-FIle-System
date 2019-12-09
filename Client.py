import socket

instructions = {}

def openFile(s, msg):
    sucServer = s.recv(1024)
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

def openTag(s, msg):
    sucServer = s.recv(1024)

    s.send(msg.encode())
    ffiles = open("files", "wb")
    input_data = s.recv(1024)
    while input_data:
        ffiles.write(input_data)
        input_data = s.recv(1024)
    print("Received")
    ffiles.close()

    ftags = open("tags", "wb")
    input_data = s.recv(1024)
    while input_data:
        ftags.write(input_data)
        input_data = s.recv(1024)
    print("Received")
    ftags.close()

def addTag(s, msg):
    sucServer = s.recv(1024)

    s.send(msg.encode())

def addFile(s, msg):
    sucServer = s.recv(1024)

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

def addFileKey(s, msg, _bool):
    sucServer = s.recv(1024)

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
    pass

def deleteTag(s, msg):
    sucServer = s.recv(1024)

    s.send(msg.encode())

def deleteFile(s, msg):
    sucServer = s.recv(1024)

    s.send(msg.encode())

def initializeInstructions():
    instructions["openFile"] = openFile
    instructions["addTag"] = addTag
    instructions['addFile'] = addFile
    instructions["deleteTag"] = deleteTag
    instructions["deleteFile"] = deleteFile
    instructions["openTag"] = openTag
    instructions["print"] = print
