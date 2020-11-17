import socket
import threading

port = 12345
max_threads = 5
max_connection_queue = 10
buffersize = 1024
host = ""

socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
socket.bind((host, port))
socket.listen(max_connection_queue)

class Handle:
    def __init__(self,message, client):
        args = message.split("\n")   
        args.pop(-1)
        self.client = client
        self.Fields_Req = {"sessionid":"None","state":"None","request":"None","form":[]}
        self.Fields_Res = {"sessionid":"None","state":"None","message":"None","form":[]}
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
    
    def decide_request(self):
        if (self.Fields_Req["sessionid"] == "None"):
            if (self.Fields_Req["state"] == "None"):
                self.Fields_Res["state"] = "acesspage"
                self.Fields_Res["message"] = "1 - SignIn\t2 - SignUp"
            if (self.Fields_Req["state"] == "acesspage"):
                if (self.Fields_Req["request"] == "1"):
                    print("")
                elif (self.Fields_Req["request"] == "2"):
                    self.Fields_Res["state"] = "signup"
                    self.Fields_Res["message"] = "Fill the following details" 
                else:
                    print("")
                    # TO DO
        
    
    def SendMessage(self):
        self.decide_request()
        msg_client = ""
        for key in self.Fields_Res:
            val = self.Fields_Res[key]
            if (val):
                msg_client += (key + ":" + val + "\n")
        size = len(msg_client)
        msg_client = str(size) + "\n" + msg_client
        self.client.send(msg_client.encode())

def handleReq(client):
    buffer = ""
    while True:
        c = client.recv(1).decode()
        if c=="\n":
            break
        buffer += c
    size = int(buffer)
    buffer = ""
    while size>len(buffer):
        buffer = buffer + client.recv(buffersize).decode()
    request = Handle(buffer,client)
    request.SendMessage()
    request.client.close()

while True:
    client, addr = socket.accept()
    Thread = threading.Thread(target=handleReq, args=(client,))
    Thread.start()