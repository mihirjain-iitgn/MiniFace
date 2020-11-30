import socket
import stdiomask
import os
import atexit


port = 12346
buffersize = 1024

path = "./test.txt"
fd = open(path, "r")

ssid = fd.readline()

fd.close()

def exit_handler():
    global ssid
    print(ssid)
    fd = open(path, "w")
    fd.write(ssid)
    fd.close()

atexit.register(exit_handler)



class Handle:
    def __init__(self,message):
        args = message.split("\n")   
        args.pop(-1)
        self.Fields_Req = {"sessionid":"None","state":"None","message":"None","form":"None"}
        self.Fields_Res = {"sessionid":"None","state":"None","request":"None","form":"None"}
        self.ExtractFields(args)

    def splitField(self,entry):
        entry1, entry2 = entry.split("(:)")
        return (entry1,entry2)
        
    def ExtractFields(self,args):
        for entry in args:
            key, value = self.splitField(entry)
            if key=="form":
                value = value.split("$")
            self.Fields_Req[key] = value
    
    def printMessage(self):
        mes = self.Fields_Req["message"].replace("\t","\n")
        if (mes):
            # os.system('clear')
            print(mes)

    def decide_request(self):
        global ssid
        if (self.Fields_Req["sessionid"]!="None"):
            ssid = self.Fields_Req["sessionid"]
            if (ssid == "SetNone"):
                ssid = "None"
        self.Fields_Res["sessionid"] = ssid
        self.Fields_Res["state"] = self.Fields_Req["state"]
        
        if(self.Fields_Req["form"][0]):
            if (self.Fields_Req["form"]!="None"):
                details = ""
                for i in self.Fields_Req["form"]:
                    if (i!="Password"):
                        print(i,":", end="")
                        ipt =  str(input()).strip()
                    else:
                        ipt = stdiomask.getpass(mask='*')
                    while(ipt=="None"):
                        print("Choose another",i)
                        ipt =  str(input()).strip()
                    details = details + ipt + "$"
                self.Fields_Res["form"] = details
            else:
                self.Fields_Res["request"] = str(input()).strip()
        
       
    def SendMessage(self, server):
        self.decide_request()
        msg_server = ""
        for key in self.Fields_Res:
            val = self.Fields_Res[key]
            if (val!="None" or key=="sessionid"):
                msg_server += (key + "(:)" + val + "\n")
        size = len(msg_server)
        msg_server = str(size) + "\n" + msg_server
        print(msg_server)
        server.send(msg_server.encode())

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
msg_server = "sessionid(:)"+ssid+"\nstate(:)None\n"
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