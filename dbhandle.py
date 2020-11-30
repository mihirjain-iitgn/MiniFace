import sqlite3
import os

DEFAULT_PATH = './users.sqlite3'

def user_table():
    connection = sqlite3.connect(DEFAULT_PATH)
    crsr = connection.cursor() 
    sql_command = """CREATE TABLE user_details (
    username,
    pwd,
    Gender,
    Age,
    sessionid,
    online);"""
    crsr.execute(sql_command) 
    connection.commit()  
    connection.close()
    return True

def friends_table():
    connection = sqlite3.connect(DEFAULT_PATH)
    crsr = connection.cursor() 
    sql_command = """CREATE TABLE friends (
    P1,
    P2,
    status);"""
    crsr.execute(sql_command) 
    connection.commit()  
    connection.close()
    return True

def posts_table():
    connection = sqlite3.connect(DEFAULT_PATH)
    crsr = connection.cursor() 
    sql_command = """CREATE TABLE posts (
    P,
    scope,
    time,
    Post);"""
    crsr.execute(sql_command) 
    connection.commit()  
    connection.close()
    return True

def message_table():
    connection = sqlite3.connect(DEFAULT_PATH)
    crsr = connection.cursor() 
    sql_command = """CREATE TABLE messages (
    P1,
    P2,
    f1,
    f2,
    time,
    status,
    message
    );"""
    crsr.execute(sql_command) 
    connection.commit()  
    connection.close()
    return True

def save_details(table,details):

    # connecting to the database
    connection = sqlite3.connect(DEFAULT_PATH)
    crsr = connection.cursor()  
    # SQL command to insert the data in the table  
    val = "("
    for _ in details:
        val+=("?,")
    val = val[:len(val)-1]
    val+=");"
    sql_command = "INSERT INTO "+ table +" VALUES " + val
    # print(sql_command)
    # print(details)
    crsr.execute(sql_command, tuple(details)) 

    connection.commit() 
    connection.close()
    return True


def fetch_posts(name1,name2,status):
    name1 = "'" + name1 + "'"
    name2 = "'" + name2 + "'"
    status = "'" + status + "'"
    connection = sqlite3.connect(DEFAULT_PATH)
    crsr = connection.cursor() 
    if(name1==name2):
        cmd = "SELECT * FROM posts WHERE P=" + name2
    else:
        if(status=="'1'"):
            cmd = "SELECT * FROM posts WHERE P=" + name2 + " AND scope!='2'"
        else:
            cmd = "SELECT * FROM posts WHERE P=" + name2 + " AND scope='0'"

    
    crsr.execute(cmd) 
    ans = crsr.fetchall()
    connection.close()
    return ans

def online_users():
    connection = sqlite3.connect(DEFAULT_PATH)
    crsr = connection.cursor()
    cmd = "SELECT username FROM user_details WHERE online='1'"
    crsr.execute(cmd)
    ans = crsr.fetchall()
    for i in range(len(ans)):
        ans[i] = list(ans[i])
        ans[i] = ans[i][0]
    connection.close()
    print(ans)
    return ans

def fetch_details(name):
    name = "'" + name + "'"
    connection = sqlite3.connect(DEFAULT_PATH)
    crsr = connection.cursor() 
    cmd = "SELECT * FROM user_details WHERE username=" + name
    crsr.execute(cmd) 

    # store all the fetched data in the ans variable 
    ans = crsr.fetchone()
    if(ans!=None):
        ans = list(ans)
        # ans = ans[:len(ans)-2]
    # print(ans)
    connection.close()
    return ans

def friends_details(p1,p2,name,status):
    name = "'" + name + "'"
    status = "'" + status + "'" 
    connection = sqlite3.connect(DEFAULT_PATH)
    crsr = connection.cursor() 
    cmd = "SELECT "+ p1 +" FROM friends WHERE " + p2 +"=" +name + " AND status="+status
    crsr.execute(cmd) 
    ans = crsr.fetchall()
    flist = []
    if(ans!=[]):
        for i in ans:
            flist.append(i[0])

    connection.close()
    return flist

def check_friends(name1,name2):
    name1 = "'" + name1 + "'"
    name2 = "'" + name2 + "'"
    connection = sqlite3.connect(DEFAULT_PATH)
    crsr = connection.cursor() 
    cmd = "SELECT status FROM friends WHERE P1=" + name1 + " AND P2=" +name2
    crsr.execute(cmd) 
    ans = crsr.fetchall()
    flist = []
    if(ans!=[]):
        for i in ans:
            flist.append(i[0])
    connection.close()
    return flist

def profile_details(ssid):
    ssid = "'" + ssid + "'" 
    connection = sqlite3.connect(DEFAULT_PATH)
    crsr = connection.cursor() 
    # print(ssid)
    cmd = "SELECT * FROM user_details WHERE sessionid=" + ssid 
    crsr.execute(cmd) 
    ans = crsr.fetchone()
    if(ans!=None):
        ans = list(ans)
        ans.pop(1)
        ans = ans[:len(ans)-2]
    # print(ans)
    connection.close()
    return ans

def update_details(username,ssid,online):
    connection = sqlite3.connect(DEFAULT_PATH)
    crsr = connection.cursor()
    username = "'" + username + "'"
    ssid = "'" + ssid + "'"
    online = "'" + online + "'"
    cmd = "UPDATE user_details SET sessionid="+ssid +", online=" + online + "WHERE username=" + username
    crsr.execute(cmd) 

    connection.commit()
    connection.close()
    return

def update_chat(user1,user2,var,value):
    user1 = "'" + user1 + "'"
    user2 = "'" + user2 + "'"
    value = "'" + value + "'"
    connection = sqlite3.connect(DEFAULT_PATH)
    crsr = connection.cursor() 
    cmd = "UPDATE messages SET " + var + "=" + value + " WHERE P1=" + user1 + " AND P2=" + user2
    crsr.execute(cmd) 

    connection.commit()
    connection.close()
    return

def accept_req(P1,P2):
    connection = sqlite3.connect(DEFAULT_PATH)
    crsr = connection.cursor()
    P1 = "'" + P1 + "'"
    P2 = "'" + P2 + "'"
    cmd = "UPDATE friends SET status='1' WHERE P1="+P1 + " AND P2="+P2
    crsr.execute(cmd) 

    connection.commit()
    connection.close()
    return

def delete_req(P1,P2):
    connection = sqlite3.connect(DEFAULT_PATH)
    crsr = connection.cursor()
    P1 = "'" + P1 + "'"
    P2 = "'" + P2 + "'"
    cmd = "DELETE from friends WHERE P1="+P1 + " AND P2="+P2
    crsr.execute(cmd) 

    connection.commit()
    connection.close()
    return

def delete_friend(P1,P2):
    connection = sqlite3.connect(DEFAULT_PATH)
    crsr = connection.cursor()
    P1 = "'" + P1 + "'"
    P2 = "'" + P2 + "'"
    cmd = "DELETE from friends WHERE (P1="+P1 + " AND P2="+P2 + ") OR (P1="+P2 + " AND P2="+P1 + ")"
    crsr.execute(cmd) 

    connection.commit()
    connection.close()
    return

def delete_post(user,post):
    connection = sqlite3.connect(DEFAULT_PATH)
    crsr = connection.cursor()
    user = "'" + user + "'"
    post = "'" + post + "'"
    cmd = "DELETE from posts WHERE P="+ user + " AND post="+post
    crsr.execute(cmd) 

    connection.commit()
    connection.close()
    return

def fetch_chats(user):
    user = "'" + user + "'"
    connection = sqlite3.connect(DEFAULT_PATH)
    crsr = connection.cursor() 
    # cmd = "SELECT P1 FROM messages WHERE status='1' AND P2=" + user
    cmd = "SELECT P1,COUNT(*) FROM messages WHERE status='1' AND P2=" + user + " GROUP BY P1"
    crsr.execute(cmd) 

    # store all the fetched data in the ans variable 
    ans = crsr.fetchall()
    connection.close()
    return ans

def getMessages(user1,user2):
    user1 = "'" + user1 + "'"
    user2 = "'" + user2 + "'"
    connection = sqlite3.connect(DEFAULT_PATH)
    crsr = connection.cursor() 
    # cmd = "SELECT P1 FROM messages WHERE status='1' AND P2=" + user
    cmd = "SELECT P1,time,status,message FROM messages WHERE ( P1=" + user1 + "  AND P2=" + user2 + " AND f1='1' ) OR ( P1=" + user2 + "  AND P2=" + user1 + " AND f2='1' )"
    crsr.execute(cmd) 

    # store all the fetched data in the ans variable 
    ans = crsr.fetchall()
    connection.close()
    return ans


# user_table()
# friends_table()
# posts_table()
# message_table()
# save_details("user_details",["Priy","kavjk","M","may","2790y08","1"])
# save_details("friends",["mihir","priyam","0"])
# print(friends_details("P1","P2","priyam","0"))
# update_details("Priy","nvaknajjb","0")
# print(fetch_chats("mihir"))
# profile_details("Priy")
# [('save this is last for the day',), ('good morning priyam',)]
# save_details("messages",["priy","profit","0","0","tame","0","msg"])
# print(fetch_chats("profit"))
# print(getMessages("a","mihir"))
