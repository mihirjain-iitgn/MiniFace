import socket

port = 12345
buffersize = 1024

class Handle:
    def __init__(self,message):
        args = message.split("\n")   
        args.pop(-1)
        # self.client = client
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
    
    def decide_request(self, user_input):
        if (self.Fields_Req["sessionid"]!="None"):
            self.Fields_Res["sessionid"] = self.Fields_Req["sessionid"]
        self.Fields_Res["request"] = user_input
        self.Fields_Res["state"] = self.Fields_Req["state"]
    
    def SendMessage(self, user_input, server):
        self.decide_request(user_input)
        msg_client = ""
        for key in self.Fields_Res:
            val = self.Fields_Res[key]
            if (val):
                msg_client += (key + ":" + val + "\n")
        size = len(msg_client)
        msg_client = str(size) + "\n" + msg_client
        server.send(msg_client.encode())

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
    return buffer

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('127.0.0.1', port))
msg_server = "sessionid:None\nstate:None\n"
msg_server = str(len(msg_server)) + "\n" + msg_server
s.send(msg_server.encode())
buffer = handleReq(s)
while(1):
    request = Handle(buffer)
    request.printMessage()
    s.close()
    user_input = input().rstrip()
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('127.0.0.1', port))
    request.SendMessage(user_input,s)
    buffer = handleReq(s)


    