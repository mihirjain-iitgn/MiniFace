import socket

port = 12345
buffersize = 1024

class Handle:
    def __init__(self,message, client):
        args = message.split("\n")   
        args.pop(-1)
        self.client = client
        self.Fields_Req = {"sessionid":"None","state":"None","message":"None","form":[]}
        self.Fields_Res = {"sessionid":"None","state":"None","request":"None","form":[]}
        self.ExtractFields(args)

    def splitField(self,entry):
        entry1, entry2 = entry.split(":")
        return (entry1,entry2)
        
    def ExtractFields(self,args):
        for entry in args:
            key, value = self.splitField(entry)
            if key=="form":
                value = value.split("\n")
            self.Fields_Req[key] = value
    
    def printMessage(self):
        print(self.Fields_Req["message"])
    
    def decide_request(self):
        if (self.Fields_Req["sessionid"]=="None" and self.Fields_Req["state"]=="None"):
            self.Fields_Res["state"] = "acesspage"
            self.Fields_Res["message"] = "1: SignIn\n2: SignUp"
    
    def SendMessage(self):
        self.decide_request()
        msg_client = ""
        for key in self.Fields_Res:
            val = self.Fields_Req[key]
            msg_client += (key + ":" + val + "\n")
        size = len(msg_client)
        msg_client = str(size) + "\n" + msg_client
        self.client.send(msg_client.encode())

def handleReq(s):
    buffer = ""
    while True:
        c = s.recv(1).decode()
        if c=="\n":
            break
        buffer += c
    size = int(buffer)
    buffer = ""
    while size>len(buffer):
        buffer = buffer + s.recv(buffersize).decode()
    request = Handle(buffer,s)
    request.printMessage()

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
s.connect(('127.0.0.1', port))

msg_server = "sessionid:None\nstate:None\n"
msg_server = str(len(msg_server)) + "\n" + msg_server
s.send(msg_server.encode())
handleReq(s)