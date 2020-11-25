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

# def session_table():
#     connection = sqlite3.connect('./users.sqlite3')
#     crsr = connection.cursor() 
#     sql_command = """CREATE TABLE session_details (
#     username,
#     sessionid,
#     online);"""
#     crsr.execute(sql_command) 
#     connection.commit()  
#     connection.close()
#     return True

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


def fetch_details(name):
    name = "'" + name + "'"
    # connect withe the myTable database 
    connection = sqlite3.connect("./users.sqlite3") 

    # cursor object 
    crsr = connection.cursor() 
    cmd = "SELECT * FROM user_details WHERE username=" + name
    # execute the command to fetch all the data from the table emp 
    crsr.execute(cmd) 

    # store all the fetched data in the ans variable 
    ans = crsr.fetchone()
    if(ans!=None):
        ans = list(ans)
        # ans = ans[:len(ans)-2]
    # print(ans)
    return ans

def profile_details(sesid):
    sesid = "'" + sesid + "'"
    # connect withe the myTable database 
    connection = sqlite3.connect("./users.sqlite3") 

    # cursor object 
    crsr = connection.cursor() 
    print(sesid)
    cmd = "SELECT * FROM user_details WHERE sessionid=" + sesid
    # execute the command to fetch all the data from the table emp 
    crsr.execute(cmd) 

    # store all the fetched data in the ans variable
     
    ans = crsr.fetchone()
    if(ans!=None):
        ans = list(ans)
        ans.pop(1)
        ans = ans[:len(ans)-2]
    print(ans)
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

# user_table()
# save_details("user_details",["Priy","kavjk","M","may","2790y08","1"])
# print(fetch_details("Priy"))
# update_details("Priy","nvaknajjb","0")
# print(fetch_details("Priy"))
# profile_details("Priy")
# [('save this is last for the day',), ('good morning priyam',)]