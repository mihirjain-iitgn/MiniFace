import sqlite3
from os.path import isfile
import os

DEFAULT_PATH = './users.sqlite3'


def user_table():
    connection = sqlite3.connect('./users.sqlite3')
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
    connection = sqlite3.connect('./users.sqlite3')
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
    connection = sqlite3.connect('./users.sqlite3')
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

def save_details(table,details):

    # connecting to the database
    if isfile(DEFAULT_PATH):
        connection = sqlite3.connect("./users.sqlite3") 
    else:
        connection = sqlite3.connect("./users.sqlite3")
    # cursor 
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
    connection = sqlite3.connect("./users.sqlite3") 
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


def fetch_details(name):
    name = "'" + name + "'"
    connection = sqlite3.connect("./users.sqlite3") 
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
    connection = sqlite3.connect("./users.sqlite3") 
    crsr = connection.cursor() 
    cmd = "SELECT "+ p1 +" FROM friends WHERE " + p2 +"=" +name + " AND status="+status
    crsr.execute(cmd) 
    ans = crsr.fetchall()
    # SELECT friend2 FROM friends WHERE friend1 = chintu AND status = "1"
    # SELECT friend1 FROM friends WHERE friend2 = chintu AND status = "1"
    # SELECT friend1 FROM friends WHERE friend2 = chintu AND status = 0
    # SELECT friend2 FROM friends WHERE friend1 = chintu AND status = 0
    flist = []
    if(ans!=[]):
        for i in ans:
            flist.append(i[0])

    print(flist)
    connection.close()
    return flist

def check_friends(name1,name2):
    name1 = "'" + name1 + "'"
    name2 = "'" + name2 + "'"
    connection = sqlite3.connect("./users.sqlite3") 
    crsr = connection.cursor() 
    cmd = "SELECT status FROM friends WHERE P1=" + name1 + " AND P2=" +name2
    crsr.execute(cmd) 
    ans = crsr.fetchall()
    flist = []
    if(ans!=[]):
        for i in ans:
            flist.append(i[0])
    print(flist)
    connection.close()
    return flist

# def mutual_friends(name1,name2):
#     name1 = "'" + name1 + "'"
#     name2 = "'" + name2 + "'"
#     connection = sqlite3.connect("./users.sqlite3") 
#     crsr = connection.cursor() 
#     SELECT p.* 
#     FROM 
#         (
#         SELECT P2 FROM friends WHERE P1=" + name1 + " AND status="'1'"
#         UNION
#         SELECT P1 FROM friends WHERE P2=" + name1 + " AND status="'1'"
#         ) AS t1
#         INNER JOIN
#         (
#         SELECT P2 FROM friends WHERE P1=" + name1 + " AND status="'1'"
#         UNION
#         SELECT P1 FROM friends WHERE P2=" + name1 + " AND status="'1'"
#         ) AS t2
#         ON t1 = t2

#         JOIN profiles p on p.id=t1.friend_id
#     cmd = "SELECT status FROM friends WHERE P1=" + name1 + " AND P2=" +name2



def profile_details(ssid):
    ssid = "'" + ssid + "'" 
    connection = sqlite3.connect("./users.sqlite3") 
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
    connection = sqlite3.connect("./users.sqlite3") 
    crsr = connection.cursor()
    username = "'" + username + "'"
    ssid = "'" + ssid + "'"
    online = "'" + online + "'"
    cmd = "UPDATE user_details SET sessionid="+ssid +", online=" + online + "WHERE username=" + username
    crsr.execute(cmd) 

    connection.commit()
    connection.close()

def accept_req(P1,P2):
    connection = sqlite3.connect("./users.sqlite3") 
    crsr = connection.cursor()
    P1 = "'" + P1 + "'"
    P2 = "'" + P2 + "'"
    cmd = "UPDATE friends SET status='1' WHERE P1="+P1 + " AND P2="+P2
    crsr.execute(cmd) 

    connection.commit()
    connection.close()

def delete_req(P1,P2):
    connection = sqlite3.connect("./users.sqlite3") 
    crsr = connection.cursor()
    P1 = "'" + P1 + "'"
    P2 = "'" + P2 + "'"
    cmd = "DELETE from friends WHERE P1="+P1 + " AND P2="+P2
    crsr.execute(cmd) 

    connection.commit()
    connection.close()

def delete_post(user,post):
    connection = sqlite3.connect("./users.sqlite3") 
    crsr = connection.cursor()
    user = "'" + user + "'"
    post = "'" + post + "'"
    cmd = "DELETE from posts WHERE P="+ user + " AND post="+post
    crsr.execute(cmd) 

    connection.commit()
    connection.close()

# user_table()
# friends_table()
# posts_table()
# save_details("user_details",["Priy","kavjk","M","may","2790y08","1"])
# save_details("friends",["mihir","priyam","0"])
# print(friends_details("P1","P2","priyam","0"))
# update_details("Priy","nvaknajjb","0")
# print(fetch_details("Priy"))
# profile_details("Priy")
# [('save this is last for the day',), ('good morning priyam',)]