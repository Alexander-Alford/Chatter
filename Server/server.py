#Modules for handling environment variables.
import os
from dotenv import load_dotenv
#Flask modules for http routing, requests, and responses.
from flask import Flask, jsonify, request
from flask_cors import CORS

from sql import SQL_Wrapper

#import boto3

#import mysql.connector



app = Flask(__name__)
CORS(app)


#AWS database environment variables.
load_dotenv()
DB_NAME = os.environ.get("AWS_DBNAME")
DB_ENDPOINT = os.environ.get("AWS_ENDPOINT")
DB_PORT = os.environ.get("AWS_PORT")
DB_REGION = os.environ.get("AWS_REGION")
DB_USERNAME = os.environ.get("AWS_USER")
DB_PASSWORD = os.environ.get("AWS_PASSWORD")


#os.environ['LIBMYSQL_ENABLE_CLEARTEXT_PLUGIN'] = '1'

#The primary wrapper that will be used to interact with the MySQL database.
sqlWrapper = SQL_Wrapper(DB_ENDPOINT, DB_USERNAME, DB_PASSWORD)





#sqlWrapper.showTable("users")
#sqlWrapper.addNewUser("test1", "123", "#FFFFFF", "#AAAAAA")
#sqlWrapper.showTable("users")
#sqlWrapper.addNewUser("test2", "123", "#FFFFFF", "#AAAAAA")
#sqlWrapper.showTable("users")
#sqlWrapper.deleteUser("test2")
#sqlWrapper.showTable("users")
#sqlWrapper.addNewUser("test2", "123", "#FFFFFF", "#AAAAAA")
#sqlWrapper.showTable("users")

#sqlWrapper.addChatMessage("test3", "test4", "This is another one.", "2234567890")
#sqlWrapper.showTable("chatlog")
#sqlWrapper.addChatMessage("test4", "test3", "Testing.", "0234567890")
sqlWrapper.showTable("users")

#sqlWrapper.deleteUserConversations("test")
sqlWrapper.showTable("chatlog")
print(sqlWrapper.readUserData("test1"))
print(sqlWrapper.readConversationLog("test3", "test4"))
#sqlWrapper.deleteDatabase("ChatterDB")


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