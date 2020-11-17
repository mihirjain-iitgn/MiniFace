import sqlite3
from os.path import isfile
import os

DEFAULT_PATH = './users.sqlite3'

def user_table():
    connection = sqlite3.connect(DEFAULT_PATH)
    crsr = connection.cursor() 
    sql_command = """CREATE TABLE user_details (
    username,
    pwd,
    Gender,
    BDay);"""
    crsr.execute(sql_command) 
    connection.commit()  
    connection.close()
    return True

def save_note(username,pwd,Gen,Bday):

    # connecting to the database
    # if(sqlite3.connect("notes.db")):
    if isfile(DEFAULT_PATH):
        connection = sqlite3.connect(DEFAULT_PATH) 
    else:
        user_table()
        connection = sqlite3.connect(DEFAULT_PATH)
    # cursor 
    crsr = connection.cursor()  

    # SQL command to insert the data in the table  
    sql_command = """INSERT INTO user_details (username,pwd,Gender,BDay) VALUES (?,?,?,?);"""
    crsr.execute(sql_command,(username,pwd,Gen,Bday,)) 

    connection.commit() 
    connection.close()
    return True

def fetch_note():
    # connect withe the myTable database 
    connection = sqlite3.connect(DEFAULT_PATH) 

    # cursor object 
    crsr = connection.cursor() 

    # execute the command to fetch all the data from the table emp 
    crsr.execute("SELECT username FROM user_details WHERE username='Priyam' ") 

    # store all the fetched data in the ans variable 
    ans = crsr.fetchall() 

    print(ans)
    return ans

# user_table()

save_note("Priyam","kavjk","M","2790y08")
fetch_note()
# [('save this is last for the day',), ('good morning priyam',)]