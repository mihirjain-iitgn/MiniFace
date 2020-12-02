import socket
import threading
from dbhandle import *
import uuid
import sys
import datetime

port = 12346
max_connection_queue = 100
buffersize = 1024
host = ""

class Handle:
    def __init__(self,message, client):
        ##Initialize the Object
        args = message.split("\n")   
        args.pop(-1)
        self.client = client
        self.Fields_Req = {"sessionid":"None","state":"None","request":"None","form":"None"}
        self.Fields_Res = {"sessionid":"None","state":"None","message":"None","form":"None"}
        self.ExtractFields(args)

    def splitField(self,entry):
        entry1, entry2 = entry.split("(:)")
        return (entry1,entry2)
        
    def ExtractFields(self,args):
        ##Extract the input of user to the form provided
        for entry in args:
            key, value = self.splitField(entry)
            if key=="form":
                value = value.split("$")
                value.pop(-1)
            self.Fields_Req[key] = value

    def profile(self,ssid):
        ##Show Your Profile
        details = profile_details(ssid)
        user = ['USERNAME','GENDER','BIRTHDAY']
        reply = ""
        for i in range(3):
            reply+=(user[i]+" : "+details[i]+"\t")
        reply+=("1.Friends\t2.Search\t3.Posts\t4.See Messages\t5.Chat\t6.Logout")
        self.Fields_Res["message"] = reply
    
    def getUsername(self,ssid):
        ##Get Username from sessionid
        return profile_details(ssid)[0]

    def profile_other(self,details):
        ##Show Profile of other User
        user = ['USERNAME','GENDER','BIRTHDAY']
        reply = ""
        for i in range(3):
            reply+=(user[i]+" : "+details[i]+"\t")
        reply+=("1.Send Request\t2.Send Message\t3.See Posts\t4.See Friends\t5.Back to Profile")
        self.Fields_Res["message"] = reply

    def checkid(self,ssid):
        ##Check Valid User Exists or not for given sessionid
        if(profile_details(ssid)):
            ## some user is assigned that session ID
            return 1
        else:
            ## Invalid session ID
            return 0

    def decide_request(self):
        if (self.Fields_Req["sessionid"] == "None"):  
            if (self.Fields_Req["state"] == "None"):
                ##Initial State
                self.Fields_Res["state"] = "acesspage"
                self.Fields_Res["message"] = "Action\t1:SignIn\t2:SignUp"
            elif (self.Fields_Req["state"] == "acesspage"):
                ##First Page
                if (self.Fields_Req["request"] == "1"):
                    ##SignInForm
                    self.Fields_Res["state"] = "signin"
                    self.Fields_Res["message"] = "Fill the following details"
                    self.Fields_Res["form"] = "Username$Password"
                elif (self.Fields_Req["request"] == "2"):
                    ##SignUPForm
                    self.Fields_Res["state"] = "signup"
                    self.Fields_Res["message"] = "Fill the following details"
                    self.Fields_Res["form"] = "Username$Password$Gender$Birthday"
                else:
                    ##Invalid Input
                    self.Fields_Res["state"] == "acesspage"
                    self.Fields_Res["message"] = "You Pressed the Wrong key.\t1:SignIn\t2:SignUp"
            elif (self.Fields_Req["state"] == "signup"):
                ##SignUP
                if (fetch_details(self.Fields_Req["form"][0])==None):
                    ##New User
                    temp = []
                    for i in self.Fields_Req["form"]:
                        temp.append(i)
                    self.Fields_Res["state"] = "profile@self"
                    self.Fields_Res["sessionid"] = (uuid.uuid1()).hex
                    temp.append(self.Fields_Res["sessionid"])
                    temp.append("1")
                    save_details("user_details",temp)
                    self.profile(self.Fields_Res["sessionid"])
                else:
                    ##Username Exists
                    self.Fields_Res["state"] = "acesspage"
                    self.Fields_Res["sessionid"] = "None"
                    self.Fields_Res["message"] = "Username is not avaliable. Try Again!\tAction\t1:SignIn\t2:SignUp"
            elif (self.Fields_Req["state"] == "signin"):
                ##SignIn
                det = fetch_details(self.Fields_Req["form"][0])
                if (det!=None):
                    ##User Found
                    if(det[1]==self.Fields_Req["form"][1]):
                        ##Login Successful
                        self.Fields_Res["state"] = "profile@self"
                        self.Fields_Res["sessionid"] = (uuid.uuid1()).hex
                        update_details(self.Fields_Req["form"][0],self.Fields_Res["sessionid"],"1")
                        self.profile(self.Fields_Res["sessionid"])
                    else:
                        ##Wrong Pwd
                        self.Fields_Res["state"] = "acesspage"
                        self.Fields_Res["sessionid"] = "None"
                        self.Fields_Res["message"] = "Wrong Credentials!\tAction\t1:SignIn\t2:SignUp"
                else:
                    ## Username does not exist
                    self.Fields_Res["state"] = "acesspage"
                    self.Fields_Res["sessionid"] = "None"
                    self.Fields_Res["message"] = "Username does not exist.Try Again!\tAction\t1:SignIn\t2:SignUp"
            else:
                self.Fields_Res["state"] = "acesspage"
                self.Fields_Res["sessionid"] = "None"
                self.Fields_Res["message"] = "You are Not Logged In.\t1:SignIn\t2:SignUp"
        else:
            ##User has provided a SessionId
            ssid = self.Fields_Req["sessionid"]
            if (self.checkid(ssid)==0):
                ##Invalid SessionID
                self.Fields_Res["state"] = "acesspage"
                self.Fields_Res["sessionid"] = "None"
                self.Fields_Res["message"] = "Invalid User.\t1:SignIn\t2:SignUp"
            else:
                ##Valid User Authentication
                if self.Fields_Req["state"]=="None":
                    self.Fields_Req["state"] = "profile@self"
                if self.Fields_Req["state"][:7]=="profile":
                    ##Profile
                    prof = self.Fields_Req["state"].split("@")[1]
                    if (prof == "self"):
                        ##Profile of User
                        if (self.Fields_Req["request"]=="1"):
                            ##Friends
                            self.Fields_Res["state"] = "friends"
                            self.Fields_Res["message"]  = "1.Your Friends\t2.Requests\t3.Requests Made by you\t4.Back to your profile"
                        elif (self.Fields_Req["request"]=="2"):
                            ##Search Other Profiles
                            self.Fields_Res["state"] = "search"
                            self.Fields_Res["message"] = "Enter the Following"
                            self.Fields_Res["form"] = "Username"
                        elif (self.Fields_Req["request"]=="3"):
                            ##See user posts
                            self.Fields_Res["state"] = "posts@self"
                            self.Fields_Res["message"] = "1.New Post\t2.See Posts\t3.Back to Profile"
                        elif (self.Fields_Req["request"]=="4"):
                            ##See Messages
                            self.Fields_Res["message"] = ""
                            self.Fields_Res["form"] = "Username$Action"
                            self.Fields_Res["state"] = "formmessage"
                            user = self.getUsername(self.Fields_Req['sessionid'])
                            readchats = fetch_readchats("P1",user)
                            readchats.extend(fetch_readchats("P2",user))
                            unreadchats = fetch_unreadchats(user)
                            temp = set(readchats)
                            for i in unreadchats:
                                if i[0] in temp:
                                    temp.remove(i[0])
                            readchats = list(temp)
                            
                            for i in range(len(unreadchats)):
                                self.Fields_Res["message"] += (str(i+1) + ". "+ str(unreadchats[i][0]) + " (" +str(unreadchats[i][1]) + ")\t")
                            n = len(unreadchats)
                            for j in range(len(readchats)):
                                self.Fields_Res["message"] += (str(n+1+j) + ". "+ str(readchats[i]) + "\t")

                            self.Fields_Res["message"] += "Action\t1.Open\t2.Delete\t3.Back to profile"
                        elif (self.Fields_Req["request"]=="5"):
                            ##Show Online Friends and Chat
                            online = set(online_users())
                            friends = []
                            username = self.getUsername(self.Fields_Req["sessionid"])
                            friends.extend(friends_details("P2","P1",username,"1"))
                            friends.extend(friends_details("P1","P2",username,"1"))
                            friends = set(friends)
                            # print(friends)
                            friends_online = online.intersection(friends)
                            friends_online = list(friends_online)
                            # print(friends_online)
                            temp = ""
                            for i in range(len(friends_online)):
                                temp += str(i+1) + ". " + friends_online[i] + "\t"
                            self.Fields_Res["message"] = temp
                            self.Fields_Res["message"] += "Action:\t0.Back to Profile\t1.Message"
                            self.Fields_Res["form"] = "Username$Action"
                            self.Fields_Res['state'] = "formmessage"

                        elif (self.Fields_Req["request"]=="6"):
                            ##Logout
                            ssid = self.Fields_Req["sessionid"]
                            user = self.getUsername(ssid)
                            self.Fields_Res["sessionid"] = "SetNone"
                            self.Fields_Res["state"] = "acesspage"
                            update_details(user,ssid,"0")
                            self.Fields_Res["message"] = "1:SignIn\t2:SignUp"
                        else:
                            self.Fields_Res["state"] = "profile@self"
                            self.profile(self.Fields_Req["sessionid"])
                    else:
                        if(self.Fields_Req["request"]=="1"):
                            ##Send Friend Request
                            details = fetch_details(prof)
                            user = self.getUsername(self.Fields_Req["sessionid"])
                            check = check_friends(user,prof)
                            self.Fields_Res["state"] = "profile@" + prof
                            self.profile_other(details)                            
                            if (not check):
                                ##Not Friend, request Sent
                                save_details("friends",[user,prof,"0"])
                                self.Fields_Res["message"] += ("\tSent\t")
                            elif(check == ["0"]):
                                ##Request already sent
                                self.Fields_Res["message"] += ("\tAlready Sent\t")
                            else:
                                ##already friends
                                self.Fields_Res["message"] +=("\tAlready Friends\t")

                        elif(self.Fields_Req["request"]=="2"):
                            ##Send message
                            self.Fields_Res["state"] = "message1@" + prof
                            self.Fields_Res["form"] = "" 
                            self.Fields_Res["message"] = "" 

                        elif(self.Fields_Req["request"]=="3"):
                            ##See Posts according to scope set by the other profile
                            user = self.getUsername(self.Fields_Req["sessionid"])
                            if (check_friends(user, prof) or check_friends(prof, user)):
                                posts = fetch_posts(user, prof,"1")
                            else:
                                posts = fetch_posts(user, prof,"0") 
                            self.Fields_Res["message"] = ""
                            self.Fields_Res["form"] = "Action"
                            self.Fields_Res["state"] = "backprof@"+prof
                            for i in range(len(posts)):
                                posts[i] = list(posts[i])
                                if(posts[i][1]=="0"):
                                    posts[i][1] = "Public"
                                elif(posts[i][1]=="1"):
                                    posts[i][1] = "Friends"
                                elif(posts[i][1]=="2"):
                                    posts[i][1] = "Private"
                                self.Fields_Res["message"] += (str(i+1)+". "+ posts[i][3]+" ("+posts[i][1]+")\tTime : "+posts[i][2]+"\t\t")
                            self.Fields_Res["message"] += "\tAction:\t1.Back to Profile\t"

                        elif(self.Fields_Req["request"]=="4"):
                            ##See Friends
                            friends = []
                            friends.extend(friends_details("P2","P1",prof,"1"))
                            friends.extend(friends_details("P1","P2",prof,"1"))
                            self.Fields_Res["message"] = "\t".join(list(friends))
                            self.Fields_Res["message"] += "\tAction:\t1.Back to Profile\t"
                            self.Fields_Res["state"] = "backprof@" + prof
                            self.Fields_Res["form"] = "Action"

                        elif(self.Fields_Req["request"]=="5"):
                            ##GO back to Self Profile
                            self.Fields_Res["state"] = "profile@self"
                            self.profile(self.Fields_Req["sessionid"])
                        else:
                            ##Profile of other user
                            self.Fields_Res["state"] = "profile@"+prof
                            details = fetch_details(prof)
                            self.profile_other(details)

                elif (self.Fields_Req["state"][0:7]=="message"):
                    des = self.Fields_Req["state"][7]
                    prof = self.Fields_Req["state"][9:]
                    temp = ""
                    if (des=="1"):
                        ##List Message
                        user = self.getUsername(self.Fields_Req["sessionid"])
                        update_chat(prof, user,"status","0")
                        messages = getMessages(user, prof)
                        for i in messages:
                            i = list(i)
                            name = i[0]
                            tame = i[1]
                            status = i[2]
                            if(status == "0"):
                                status = "Read"
                            elif(status =="1"):
                                status = "Unread"
                            message = i[3]
                            temp += (name + ": " +message + " ("+ status + ")   " + tame + "\t")
                        self.Fields_Res["message"] = temp
                        self.Fields_Res["message"] += "\tAction:\t1.Message\t2.Back to Profile"
                        self.Fields_Res["state"] = "message2@" + prof
                        self.Fields_Res["form"] = "Message$Action"
                    else:
                        ##Add New Message
                        user = self.getUsername(self.Fields_Req["sessionid"])
                        action = self.Fields_Req["form"][1]
                        if (action=="1"):
                            message = self.Fields_Req["form"][0]
                            user = self.getUsername(self.Fields_Req["sessionid"])
                            update_chat(prof, user,"status","0")
                            tame = datetime.datetime.now()
                            tame = str(tame.strftime("%b %d %Y %H:%M:%S"))
                            data = [user, prof, "1", "1", tame, "1", message]
                            save_details("messages",data)
                            self.Fields_Res["state"] = "message1@" + prof
                            messages = getMessages(user, prof)
                            for i in messages:
                                i = list(i)
                                name = i[0]
                                tame = i[1]
                                status = i[2]
                                if(status == "0"):
                                    status = "Read"
                                elif(status =="1"):
                                    status = "Unread"
                                message = i[3]
                                temp += (name + ": " +message + " ("+ status + ")   " + tame + "\t")
                            self.Fields_Res["message"] = temp
                            self.Fields_Res["form"] = ""
                        else:
                            ##Go to Self Profile
                            self.Fields_Res["state"] = "profile@self"
                            self.profile(self.Fields_Req["sessionid"])
                
                elif (self.Fields_Req["state"]=="formmessage"):
                    ##Message Form Validation
                    action = self.Fields_Req["form"][1]
                    prof = self.Fields_Req["form"][0]
                    if (action=="1"):
                        self.Fields_Res["state"] = "message1@" + prof
                        user = self.getUsername(self.Fields_Req["sessionid"])
                        update_chat(prof, user,"status","0")
                        self.Fields_Res["form"] = ""
                    elif (action=="2"):
                        ##Delete Message
                        update_chat(prof, user,"f2","0")
                        update_chat(user, prof,"f1","0")
                        self.Fields_Res["state"] = "profile@self"
                        self.profile(self.Fields_Req["sessionid"])
                    else:
                        ##Invalid Input
                        self.Fields_Res["state"] = "profile@self"
                        self.profile(self.Fields_Req["sessionid"])   

                elif (self.Fields_Req["state"]=="search"):
                    username = self.Fields_Req["form"][0]
                    user = self.getUsername(self.Fields_Req["sessionid"])
                    details = fetch_details(username)
                    if(details==None or user==username):
                        ##No user found
                        self.Fields_Res["state"] = "search"                    
                        self.Fields_Res["message"] = "No user Found"
                        self.Fields_Res["form"] = "Username"
                    else:
                        ##user Found
                        self.Fields_Res["state"] = "profile@" + username
                        self.profile_other(details)
            
                elif (self.Fields_Req["state"]=="friends"):
                    username = self.getUsername(self.Fields_Req["sessionid"])
                    friends = []
                    if(self.Fields_Req["request"]=="1"):
                        ##Show Friends
                        self.Fields_Res["state"] = "Friendlist"
                        self.Fields_Res["message"] = "Your Friend List\t"
                        self.Fields_Res["form"] = "Username$Action"
                        friends.extend(friends_details("P2","P1",username,"1"))
                        friends.extend(friends_details("P1","P2",username,"1"))
                        self.Fields_Res["message"] += "\t".join(list(friends))
                        self.Fields_Res["message"] += "\tAction:\t1.Go to Friend's profile\t2.Delete Friend\t3.Go to Self Profile"
                    elif(self.Fields_Req["request"]=="2"):
                        ##Show Friend Requests
                        self.Fields_Res["message"] = "Friend Requests\t"
                        self.Fields_Res["state"] = "FriendReq"
                        self.Fields_Res["form"] = "Username$Action"
                        friends.extend(friends_details("P1","P2",username,"0"))
                        self.Fields_Res["message"] += "\t".join(list(friends))
                        self.Fields_Res["message"] += "\tAction:\t1.Accept and go to profile\t2.Delete Request\t3.Go to Self Profile"
                    elif(self.Fields_Req["request"]=="3"):
                        ##Show Sent Requests
                        self.Fields_Res["state"] = "PendReq"
                        self.Fields_Res["message"] = "Pending Requests\t"
                        friends.extend(friends_details("P2","P1",username,"0"))
                        self.Fields_Res["form"] = "Username$Action"
                        self.Fields_Res["message"] += "\t".join(list(friends))
                        self.Fields_Res["message"] += "\tAction:\t1.Go to Profile\t2.Delete Request\t3.Go to Self Profile"
                    else:
                        ##Back to Profile
                        self.Fields_Res["state"] = "profile@self"
                        self.profile(self.Fields_Req["sessionid"])

                elif (self.Fields_Req["state"]=="Friendlist"):
                    action = self.Fields_Req["form"][1]
                    prof = self.Fields_Req["form"][0]
                    if (action=="1"):
                        ##Go to Friend's Profile
                        details = fetch_details(prof)
                        if(details!=None):
                            self.Fields_Res["state"] = "profile@" + prof
                            self.profile_other(details)
                        else:
                            ##Invalid Request
                            self.Fields_Res["state"] = "friends"
                            self.Fields_Res["message"]  = "1.Your Friends\t2.Requests\t3.Requests Made by you\t4.Back to your profile"
                    elif(action=="2"):
                        ##Unfriend
                        user = self.getUsername(self.Fields_Req["sessionid"])
                        delete_friend(user,prof)
                        self.Fields_Res["state"] = "profile@" + prof
                        self.profile(self.Fields_Req["sessionid"])
                    elif(action=="3"):
                        ##Go to Self Profile
                        self.Fields_Res["state"] = "profile@self"
                        self.profile(self.Fields_Req["sessionid"])
                    else:
                        ##Invalid Request
                        self.Fields_Res["state"] = "friends"
                        self.Fields_Res["message"]  = "1.Your Friends\t2.Requests\t3.Requests Made by you\t4.Back to your profile"
            
                elif (self.Fields_Req["state"]=="FriendReq"):
                    fname,action = self.Fields_Req["form"]
                    user = self.getUsername(self.Fields_Req["sessionid"])
                    if(action=="1"):
                        ##Accept Friend Request
                        accept_req(fname, user)
                        self.profile_other(fetch_details(fname))
                        self.Fields_Res["state"] = "profile@"+fname
                    elif(action=="2"):
                        ##Delete Request
                        delete_req(fname, user)
                        self.profile(self.Fields_Req["sessionid"])
                        self.Fields_Res["state"] = "profile@self"
                    elif(action=="3"):
                        ##Go to Self Profile
                        self.Fields_Res["state"] = "profile@self"
                        self.profile(self.Fields_Req["sessionid"])
                    else:
                        ##Invalid Request
                        self.Fields_Res["state"] = "friends"
                        self.Fields_Res["message"]  = "1.Your Friends\t2.Requests\t3.Requests Made by you\t4.Back to your profile"
                
                elif (self.Fields_Req["state"]=="PendReq"):
                    fname,action = self.Fields_Req["form"]
                    user = self.getUsername(self.Fields_Req["sessionid"])
                    if(action=="1"):
                        ##Go to Friend's profile
                        self.profile_other(fetch_details(fname))
                        self.Fields_Res["state"] = "profile@"+fname
                    elif(action=="2"):
                        delete_req(user, fname)
                        self.profile(self.Fields_Req["sessionid"])
                        self.Fields_Res["state"] = "profile@self"
                    elif(action=="3"):
                        ##Go to Self Profile
                        self.Fields_Res["state"] = "profile@self"
                        self.profile(self.Fields_Req["sessionid"])
                    else:
                        ##Invalid Request
                        self.Fields_Res["state"] = "friends"
                        self.Fields_Res["message"]  = "1.Your Friends\t2.Requests\t3.Requests Made by you\t4.Back to your profile"
                        
                elif (self.Fields_Req["state"]=="posts@self"):
                    if (self.Fields_Req["request"]=="1"):
                        ##NewPost
                        self.Fields_Res["state"] = "newpost"
                        self.Fields_Res["message"]  = "Fill The Following\tScope 0 : Public, 1 : Friends, 2 : Private"
                        self.Fields_Res["form"]  = "Post$Scope"
                    elif (self.Fields_Req["request"]=="2"):
                        ##See Posts
                        self.Fields_Res["state"] = "seepostform"
                        user  = self.getUsername(self.Fields_Req["sessionid"])
                        posts = fetch_posts(user,user,"1")
                        self.Fields_Res["message"] = ""
                        self.Fields_Res["form"] = "Post Number$Action"
                        for i in range(len(posts)):
                            posts[i] = list(posts[i])
                            if(posts[i][1]=="0"):
                                posts[i][1] = "Public"
                            elif(posts[i][1]=="1"):
                                posts[i][1] = "Friends"
                            elif(posts[i][1]=="2"):
                                posts[i][1] = "Private"
                            self.Fields_Res["message"] += (str(i+1)+". "+ posts[i][3]+" ("+posts[i][1]+")\tTime : "+posts[i][2]+"\t\t")

                        self.Fields_Res["message"] += "Action:\t0.Delete\t1.Back to Profile\t"
                    else:
                        ##Back To Profile
                        self.Fields_Res["state"] = "profile@self"
                        self.profile(self.Fields_Req["sessionid"])
                elif (self.Fields_Req["state"]=="newpost"):
                    ##Save New Post
                    self.Fields_Res["state"] = "posts@self"
                    self.Fields_Res["message"] = "1.New Post\t2.See Posts\t3.Back to Profile"
                    post,scope = self.Fields_Req["form"]
                    user  = self.getUsername(self.Fields_Req["sessionid"])
                    tame = datetime.datetime.now()
                    tame = str(tame.strftime("%b %d %Y %H:%M:%S"))
                    save_details("posts",[user,scope,tame,post])     
                             
                elif (self.Fields_Req["state"]=="seepostform"):
                    if(self.Fields_Req["form"][1]=="0"):
                        ##Delete a Post
                        self.Fields_Res["state"] = "posts@self"
                        self.Fields_Res["message"] = "1.New Post\t2.See Posts\t3.Back to Profile"
                        user = self.getUsername(self.Fields_Req["sessionid"])
                        posts = fetch_posts(user,user,"1")
                        post = posts[int(self.Fields_Req["form"][0])-1][3]
                        delete_post(user,post)
                    else:
                        ##Back to Profile
                        self.Fields_Res["state"] = "profile@self"
                        self.profile(self.Fields_Req["sessionid"])

                elif (self.Fields_Req["state"][:8]=="backprof"):
                    ##Profile of other user
                    prof = self.Fields_Req["state"].split("@")[1]
                    self.Fields_Res["state"] = "profile@" + prof
                    self.profile_other(fetch_details(prof))


    def SendMessage(self):
        self.decide_request()
        msg_client = ""
        for key in self.Fields_Res:
            val = self.Fields_Res[key]
            if (val!="None"):
                msg_client += (key + "(:)" + val + "\n")
        size = len(msg_client)
        msg_client = str(size) + "\n" + msg_client
        # print(msg_client)
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

def main():
    print("Server is Running...")
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    # socket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,True)
    # socket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEPORT,True)
    sock.bind((host, port))
    sock.listen(max_connection_queue)

    while True:
        try:
            client, addr = sock.accept()
            Thread = threading.Thread(target=handleReq, args=(client,))
            Thread.start()
        except:
            sock.close()
            sys.exit(0)

main()
