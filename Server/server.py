#Modules for handling environment variables.
import os
from dotenv import load_dotenv
#Flask modules for http routing, requests, and responses.
from flask import Flask, jsonify, request
from flask_cors import CORS

#import boto3
import mysql.connector



app = Flask(__name__)
CORS(app)
load_dotenv()

#AWS database environment variables.
DB_NAME = os.environ.get("AWS_DBNAME")
DB_ENDPOINT = os.environ.get("AWS_ENDPOINT")
DB_PORT = os.environ.get("AWS_PORT")
DB_REGION = os.environ.get("AWS_REGION")
DB_USERNAME = os.environ.get("AWS_USER")
DB_PASSWORD = os.environ.get("AWS_PASSWORD")


#os.environ['LIBMYSQL_ENABLE_CLEARTEXT_PLUGIN'] = '1'



sql_database = mysql.connector.connect(
  host=DB_ENDPOINT,
  user=DB_USERNAME,
  password=DB_PASSWORD
)

Cursor = sql_database.cursor()

Cursor.execute("SHOW DATABASES")

#for x in Cursor:
#  print(x) 

sqllist = Cursor.fetchall()

print(sqllist)

test = [ x[0] for x in sqllist ] 

print(test)


if "ChatterDB" in test:
    print("One")
else:
    Cursor.execute("CREATE DATABASE ChatterDB")

sql_database = mysql.connector.connect(
  host=DB_ENDPOINT,
  user=DB_USERNAME,
  password=DB_PASSWORD,
  database="ChatterDB"
)

Cursor = sql_database.cursor()

Cursor.execute("SHOW TABLES")

test = [ x[0] for x in Cursor.fetchall() ] 

if "users" in test:
    print("Two")    
else:
    Cursor.execute("CREATE TABLE users (username VARCHAR(50) NOT NULL, password VARCHAR(50) NOT NULL, primarycolor CHAR(7), secondarycolor CHAR(7), PRIMARY KEY(username))")

if "chatlog" in test:
    print("Three")
else:
    Cursor.execute("CREATE TABLE chatlog (sender VARCHAR(50), reciever VARCHAR(50), content TINYTEXT, timestamp INT UNSIGNED)")

Cursor.execute("SHOW TABLES")

for x in Cursor:
    print(x)


#Server variables.
client = ''
host = '127.0.0.1'
port = 500
chattersOnline = []


#Class hold's individual chatter's info.
class Chatter:
    def __init__(primCol, secCol, name, authToken):
        self.primaryColor = primCol
        self.secondaryColor = secCol
        self.username = name
        self.authenticationToken = authToken
    
    #Checks a chatter's authentication token versus one given from client.
    def checkAuthToken(recieved):
        if recieved == self.authenticationToken:
            return True
        else:
            return False



    

    


    




@app.route('/api/signin', methods=['GET', 'POST'])
def welcome():
    print('Hit on the sign-in api.')
    return "Hello World!"
    
@app.route('/api/chatroom', methods=['GET', 'POST'])
def manageChat():
    print('Hit on the chat room api.')
    return "Hello World!"



if __name__ == '__main__':
    app.run(host=host, port=port)