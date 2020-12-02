import socket
import stdiomask
import os
import sys
import atexit

def prYellow(skk): print("\033[93m {}\033[00m" .format(skk),":", end="")

def exit_handler():
    if (ssid!="None"):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host, port))
        msg_server = "sessionid(:)"+ssid+"\nstate(:)offline\n"
        msg_server = str(len(msg_server)) + "\n" + msg_server
        s.send(msg_server.encode())
        fd = open(path, "w")
        fd.write(ssid)
        fd.close()

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
        ##Extract values from server message
        for entry in args:
            key, value = self.splitField(entry)
            if key=="form":
                value = value.split("$")
            self.Fields_Req[key] = value
    
    def printMessage(self):
        ##Print Message
        mes = self.Fields_Req["message"].replace("\t","\n")
        if (mes):
            os.system('clear')
            print(mes)

    def decide_request(self):
        ##Taking user request as input
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
                    prYellow(i)
                    if (i!="Password"):
                        # print(i,":", end="")
                        ipt =  str(input()).strip()
                    else:
                        ipt = stdiomask.getpass(prompt="",mask='*')
                    while(ipt=="None"):
                        print("Choose another",i)
                        ipt =  str(input()).strip()
                    details = details + ipt + "$"
                self.Fields_Res["form"] = details
            else:
                self.Fields_Res["request"] = str(input("")).strip()
        
       
    def SendMessage(self, server):
        ##Form message for server
        self.decide_request()
        msg_server = ""
        for key in self.Fields_Res:
            val = self.Fields_Res[key]
            if (val!="None" or key=="sessionid"):
                msg_server += (key + "(:)" + val + "\n")
        size = len(msg_server)
        msg_server = str(size) + "\n" + msg_server
        # print(msg_server)
        server.send(msg_server.encode())

def handleReq(s):
    ##Handle the response from the server
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


def main():
    ##start client
   
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    msg_server = "sessionid(:)"+ssid+"\nstate(:)None\n"
    msg_server = str(len(msg_server)) + "\n" + msg_server
    s.send(msg_server.encode())
    buffer = handleReq(s)

    while(1):
        request = Handle(buffer)
        request.printMessage()
        s.close()
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host, port))
        request.SendMessage(s)
        buffer = handleReq(s)


buffersize = 1024
port = 12346
host = "10.0.0.1"
atexit.register(exit_handler)
path = "./test.txt"
fd = open(path, "r")
ssid = fd.readline()
ssid = "None"
fd.close()
main()
