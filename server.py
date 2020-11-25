import socket
import threading
from dbhandle import *
import uuid

port = 12345
max_threads = 5
max_connection_queue = 10
buffersize = 1024
host = ""

class Handle:
    def __init__(self,message, client):
        args = message.split("\n")   
        args.pop(-1)
        self.client = client
        self.Fields_Req = {"sessionid":"None","state":"None","request":"None","form":"None"}
        self.Fields_Res = {"sessionid":"None","state":"None","message":"None","form":"None"}
        self.ExtractFields(args)

    def splitField(self,entry):
        entry1, entry2 = entry.split(":")
        return (entry1,entry2)
        
    def ExtractFields(self,args):
        for entry in args:
            key, value = self.splitField(entry)
            if key=="form":
                value = value.split("$")
                value.pop(-1)
            self.Fields_Req[key] = value

    def profile(self):
        sessionid = self.Fields_Req["sessionid"]
        details = profile_details(sessionid)
        # print(details)
        user = ['USERNAME','GENDER','AGE']
        reply = ""
        for i in range(3):
            reply+=(user[i]+"-"+details[i]+"@")
        reply+=("1 - Friends @2 - Posts")
        self.Fields_Res["message"] = reply
    
    def decide_request(self):
        if (self.Fields_Req["sessionid"] == "None"):
            if (self.Fields_Req["state"] == "None"):
                self.Fields_Res["state"] = "acesspage"
                self.Fields_Res["message"] = "1 - SignIn\t2 - SignUp"
            elif (self.Fields_Req["state"] == "acesspage"):
                if (self.Fields_Req["request"] == "1"):
                    self.Fields_Res["state"] = "signin"
                    self.Fields_Res["message"] = "Fill the following details"
                    self.Fields_Res["form"] = "username$password"
                elif (self.Fields_Req["request"] == "2"):
                    self.Fields_Res["state"] = "signup"
                    self.Fields_Res["message"] = "Fill the following details"
                    self.Fields_Res["form"] = "username$password$gender$age"
                else:
                    print("")
                    # TO DO
            elif (self.Fields_Req["state"] == "signup"):
                if (fetch_details(self.Fields_Req["form"][0])==None):
                    temp = []
                    for i in self.Fields_Req["form"]:
                        temp.append(i)
                    self.Fields_Res["state"] = "profile"
                    self.Fields_Res["sessionid"] = (uuid.uuid1()).hex
                    self.Fields_Req["sessionid"] = self.Fields_Res["sessionid"]
                    temp.append(self.Fields_Res["sessionid"])
                    temp.append("1")
                    # print(temp)
                    save_details("user_details",temp)
                    self.profile()
                else:
                    self.Fields_Res["state"] = "signup"
                    self.Fields_Res["message"] = "Username is not avaliable. Try Again"
                    self.Fields_Res["form"] = "username$password$gender$age"
            elif (self.Fields_Req["state"] == "signin"):
                det = fetch_details(self.Fields_Req["form"][0])
                if (det!=None):
                    if(det[1]==self.Fields_Req["form"][1]):
                        self.Fields_Res["state"] = "profile"
                        self.Fields_Res["sessionid"] = (uuid.uuid1()).hex
                        self.Fields_Req["sessionid"] = self.Fields_Res["sessionid"]
                        update_details(self.Fields_Req["form"][0],self.Fields_Req["sessionid"],"1")
                        self.profile()
                    else:
                        self.Fields_Res["state"] = "signin"
                        self.Fields_Res["message"] = "Wrong Credentials!"
                        self.Fields_Res["form"] = "username$password"

                else:
                    self.Fields_Res["state"] = "signin"
                    self.Fields_Res["message"] = "Username is not avaliable. Try Again"
                    self.Fields_Res["form"] = "username$password"


    def SendMessage(self):
        self.decide_request()
        msg_client = ""
        for key in self.Fields_Res:
            val = self.Fields_Res[key]
            if (val!="None"):
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

socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
socket.bind((host, port))
socket.listen(max_connection_queue)


while True:
    client, addr = socket.accept()
    Thread = threading.Thread(target=handleReq, args=(client,))
    Thread.start()