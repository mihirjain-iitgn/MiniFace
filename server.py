import socket
import threading
from dbhandle import *
import uuid
import datetime

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

    def profile(self,ssid):
        details = profile_details(ssid)
        user = ['USERNAME','GENDER','AGE']
        reply = ""
        for i in range(3):
            reply+=(user[i]+"-"+details[i]+"\t")
        reply+=("1.Friends\t2.Search\t3.Posts")
        self.Fields_Res["message"] = reply
    
    def getUsername(self,ssid):
        return profile_details(ssid)[0]

    def profile_other(self,details):
        user = ['USERNAME','GENDER','AGE']
        reply = ""
        for i in range(3):
            reply+=(user[i]+"-"+details[i]+"\t")
        reply+=("1.Send Request\t2.Send Message\t3.See Posts\t4.See Mutual Friends\t5.Back to Profile")
        self.Fields_Res["message"] = reply

    def checkid(self,ssid):
        if(profile_details(ssid)):
            return 1
        return 0

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
                    self.Fields_Res["state"] = "profile@self"
                    self.Fields_Res["sessionid"] = (uuid.uuid1()).hex
                    temp.append(self.Fields_Res["sessionid"])
                    temp.append("1")
                    # print(temp)
                    save_details("user_details",temp)
                    self.profile(self.Fields_Res["sessionid"])
                else:
                    self.Fields_Res["state"] = "signup"
                    self.Fields_Res["message"] = "Username is not avaliable. Try Again"
                    self.Fields_Res["form"] = "username$password$gender$age"
            elif (self.Fields_Req["state"] == "signin"):
                det = fetch_details(self.Fields_Req["form"][0])
                if (det!=None):
                    if(det[1]==self.Fields_Req["form"][1]):
                        self.Fields_Res["state"] = "profile@self"
                        self.Fields_Res["sessionid"] = (uuid.uuid1()).hex
                        update_details(self.Fields_Req["form"][0],self.Fields_Res["sessionid"],"1")
                        self.profile(self.Fields_Res["sessionid"])
                    else:
                        self.Fields_Res["state"] = "signin"
                        self.Fields_Res["message"] = "Wrong Credentials!"
                        self.Fields_Res["form"] = "username$password"
                else:
                    self.Fields_Res["state"] = "signin"
                    self.Fields_Res["message"] = "Username is not avaliable. Try Again"
                    self.Fields_Res["form"] = "username$password"
            else:
                # Do something
                print("Yeh print hora h")
        # state : profile@self
        # 1. Friend
        # 2. Search
        # 3. Posts
        # 4. See Message
        # 5. Logout
        # state : profile@priyam
        # 1. Send Req
        # 2. Send Message
        # 3. See Priyam's Posts
        # 4. See Mutual Friends
        # 5. Self
        else:
            #user ki info nikaal le
            ssid = self.Fields_Req["sessionid"]
            if (self.checkid(ssid)==0):
                print("yeh hora h kya print")
            else:
                if self.Fields_Req["state"][:7]=="profile":
                    prof = self.Fields_Req["state"].split("@")[1]
                    if (prof == "self"):
                        if (self.Fields_Req["request"]=="1"):
                            self.Fields_Res["state"] = "friends"
                            self.Fields_Res["message"]  = "1.Your Friends\t2.Requests\t3.Requests Made by you"
                        elif (self.Fields_Req["request"]=="2"):
                            self.Fields_Res["state"] = "search"
                            self.Fields_Res["message"] = "Enter the Following"
                            self.Fields_Res["form"] = "Search by Username"
                        elif (self.Fields_Req["request"]=="3"):
                            self.Fields_Res["state"] = "posts@self"
                            self.Fields_Res["message"] = "1. New Post\t2. See Posts\t3. Profile"
                        
                    else:
                        if(self.Fields_Req["request"]=="1"):
                            #check if friend hai ya nhi
                            self.Fields_Res["state"] = self.Fields_Req["state"]
                            details = fetch_details(prof)
                            self.profile_other(details)
                            user = self.getUsername(self.Fields_Req["sessionid"])
                            check = check_friends(user,prof)                            
                            if (not check):
                                save_details("friends",[user,prof,"0"])
                                self.Fields_Res["message"] += ("\tSent\t")
                            elif(check == ["0"]):
                                self.Fields_Res["message"] += ("\tAlready Sent\t")
                            else:
                                self.Fields_Res["message"] +=("\tAlready Friends\t")
                        elif(self.Fields_Req["request"]=="3"):
                            user = self.getUsername(self.Fields_Req["sessionid"])
                            if (check_friends(user, prof) or check_friends(prof, user)):
                                posts = fetch_posts(user, prof,"1")
                            else:
                                posts = fetch_posts(user, prof,"0") 
                            self.Fields_Res["message"] = "1.Back to Profile\t"
                            self.Fields_Res["form"] = "Action"
                            self.Fields_Res["state"] = "backprof"
                            for i in range(len(posts)):
                                self.Fields_Res["message"] += ("Number- "+str(i+1)+"\tScope- "+posts[i][1]+"\tTime- "+posts[i][2]+"\tPost- "+posts[i][3]+"\t")
                        elif(self.Fields_Req["request"]=="4"):
                            user = self.getUsername(self.Fields_Req["sessionid"])
                            friends = []
                            friends.extend(friends_details("P2","P1",user,"1"))
                            friends.extend(friends_details("P1","P2",user,"1"))                            
                            # https://www.w3schools.com/sql/sql_join.asp
                            # https://stackoverflow.com/questions/14529454/mutual-friends-sql-algorithm

                                

                elif (self.Fields_Req["state"]=="search"):
                    username = self.Fields_Req["form"][0]
                    details = fetch_details(username)
                    if(details==None):
                        self.Fields_Res["state"] = "search"                    
                        self.Fields_Res["message"] = "No user Found"
                        self.Fields_Res["form"] = "Search by Username"
                    else:
                        self.Fields_Res["state"] = "profile@" + username
                        self.profile_other(details)
            
                elif (self.Fields_Req["state"]=="friends"):
                    username = self.getUsername(self.Fields_Req["sessionid"])
                    friends = []
                    if(self.Fields_Req["request"]=="1"):
                        self.Fields_Res["state"] = "Friendlist"
                        self.Fields_Res["message"] = "Your Friend List\t"
                        self.Fields_Res["form"] = "username"
                        friends.extend(friends_details("P2","P1",username,"1"))
                        friends.extend(friends_details("P1","P2",username,"1"))
                    elif(self.Fields_Req["request"]=="2"):
                        self.Fields_Res["message"] = "Friend Requests\t"
                        self.Fields_Res["state"] = "FriendReq"
                        self.Fields_Res["form"] = "username$action"
                        friends.extend(friends_details("P1","P2",username,"0"))
                    elif(self.Fields_Req["request"]=="3"):
                        self.Fields_Res["state"] = "PendReq"
                        self.Fields_Res["message"] = "Pending Requests\t"
                        friends.extend(friends_details("P2","P1",username,"0"))
                        self.Fields_Res["form"] = "username$action"
                    self.Fields_Res["message"] += "\t".join(list(friends))

                elif (self.Fields_Req["state"]=="Friendlist"):
                    username = self.Fields_Req["form"][0]
                    details = fetch_details(username)
                    self.Fields_Res["state"] = "profile@" + username
                    self.profile_other(details)
                elif (self.Fields_Req["state"]=="FriendReq"):
                    fname,action = self.Fields_Req["form"]
                    user = self.getUsername(self.Fields_Req["sessionid"])
                    if(action=="1"):
                        #####same time accept delete
                        accept_req(fname, user)
                        self.profile_other(fetch_details(fname))
                        self.Fields_Res["state"] = "profile@"+fname
                    elif(action=="0"):
                        #####same time accept delete
                        delete_req(fname, user)
                        self.profile(self.Fields_Req["sessionid"])
                        self.Fields_Res["state"] = "profile@self"
                    else:
                        self.profile(self.Fields_Req["sessionid"])
                        self.Fields_Res["state"] = "profile@self"
                elif (self.Fields_Req["state"]=="PendReq"):
                    fname,action = self.Fields_Req["form"]
                    user = self.getUsername(self.Fields_Req["sessionid"])
                    if(action=="1"):
                        self.profile_other(fetch_details(fname))
                        self.Fields_Res["state"] = "profile@"+fname
                    else:
                        delete_req(user, fname)
                        self.profile(self.Fields_Req["sessionid"])
                        self.Fields_Res["state"] = "profile@self"
                        
                elif (self.Fields_Req["state"]=="posts@self"):
                    prof = self.Fields_Req["state"].split("@")[1]
                    if (self.Fields_Req["request"]=="1"):
                        self.Fields_Res["state"] = "newpost"
                        self.Fields_Res["message"]  = "Fill The Following\t Scope 0 --> Public, 1 --> Friends, 2--> Private"
                        self.Fields_Res["form"]  = "Post$Scope"
                    elif (self.Fields_Req["request"]=="2"):
                        self.Fields_Res["state"] = "seepostform"
                        user  = self.getUsername(self.Fields_Req["sessionid"])
                        posts = fetch_posts(user,user,"1")
                        self.Fields_Res["message"] = "0.Delete\t1.Back to Profile\t"
                        self.Fields_Res["form"] = "Post Number$Action"
                        for i in range(len(posts)):
                            self.Fields_Res["message"] += ("Number- "+str(i+1)+"\tScope- "+posts[i][1]+"\tTime- "+posts[i][2]+"\tPost- "+posts[i][3]+"\t")
                    elif (self.Fields_Req["request"]=="3"):
                        self.Fields_Res["state"] = "profile@self"
                        self.profile(self.Fields_Req["sessionid"])
                    else:
                        print("")
                elif (self.Fields_Req["state"]=="newpost"):
                    self.Fields_Res["state"] = "profile@self"
                    post,scope = self.Fields_Req["form"]
                    user  = self.getUsername(self.Fields_Req["sessionid"])
                    tame = str(datetime.datetime.now())
                    tame = tame.replace(":","|")
                    save_details("posts",[user,scope,tame,post])
                    self.profile(self.Fields_Req["sessionid"])                    
                elif (self.Fields_Req["state"]=="seepostform"):
                    if(self.Fields_Req["form"][1]=="0"):
                        user = self.getUsername(self.Fields_Req["sessionid"])
                        posts = fetch_posts(user,user,"1")
                        post = posts[int(self.Fields_Req["form"][0])-1][3]
                        delete_post(user,post)
                    self.Fields_Res["state"] = "profile@self"
                    self.profile(self.Fields_Req["sessionid"])

                elif (self.Fields_Req["state"]=="backprof"):
                    if(self.Fields_Req["form"][0]=="1"):
                        self.Fields_Res["state"] = "profile@self"
                        self.profile(self.Fields_Req["sessionid"])
                    else:
                        print("")
    def SendMessage(self):
        self.decide_request()
        msg_client = ""
        for key in self.Fields_Res:
            val = self.Fields_Res[key]
            if (val!="None"):
                msg_client += (key + ":" + val + "\n")
        size = len(msg_client)
        msg_client = str(size) + "\n" + msg_client
        print(msg_client)
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