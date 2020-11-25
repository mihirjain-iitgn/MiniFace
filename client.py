import socket

port = 12345
buffersize = 1024

class Handle:
    def __init__(self,message):
        args = message.split("\n")   
        args.pop(-1)
        # self.client = client
        self.Fields_Req = {"sessionid":"None","state":"None","message":"None","form":"None"}
        self.Fields_Res = {"sessionid":"None","state":"None","request":"None","form":"None"}
        self.ExtractFields(args)

    def splitField(self,entry):
        entry1, entry2 = entry.split(":")
        return (entry1,entry2)
        
    def ExtractFields(self,args):
        for entry in args:
            key, value = self.splitField(entry)
            if key=="form":
                value = value.split("$")
            self.Fields_Req[key] = value
    
    def printMessage(self):
        mes = self.Fields_Req["message"].replace("@","\n")
        print("\033c")
        print(mes)
    def decide_request(self):
        if (self.Fields_Req["form"]!="None"):
            details = ""
            for i in self.Fields_Req["form"]:
                print(i,":", end="")
                ipt =  str(input()).strip()
                while(ipt=="None"):
                    print("Choose another",i)
                    ipt =  str(input()).strip()
                details = details + ipt + "$"
            self.Fields_Res["form"] = details
        else:
            self.Fields_Res["request"] = input().strip()
        if (self.Fields_Req["sessionid"]!="None"):
            self.Fields_Res["sessionid"] = self.Fields_Req["sessionid"]
        self.Fields_Res["state"] = self.Fields_Req["state"]
    
    def SendMessage(self, server):
        self.decide_request()
        msg_client = ""
        for key in self.Fields_Res:
            val = self.Fields_Res[key]
            if (val!="None" or key=="sessionid"):
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
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('127.0.0.1', port))
    request.SendMessage(s)

    buffer = handleReq(s)
