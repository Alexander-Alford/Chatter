#Modules for handling environment variables.
import os
from dotenv import load_dotenv
#Flask modules for http routing, requests, and responses.
from flask import Flask, jsonify, request
from flask_cors import CORS

from sql import SQL_Wrapper

#Imports to provide funcionality for creating session tokens.
import random
import string
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
#sqlWrapper.showTable("users")

#sqlWrapper.deleteUserConversations("test")
#sqlWrapper.showTable("chatlog")
#print("User test1 Data:")
#print(sqlWrapper.readUserData("test1"))
#print("Conversation between test3 and test4:")
#print(sqlWrapper.readConversationLog("test3", "test4"))
#sqlWrapper.updatePrimaryColor("test2", "#BBBBBB")
#sqlWrapper.updateSecondaryColor("test2", "#BBBBBB")
#print("User test1 Data:")
#print(sqlWrapper.readUserData("test1"))
#sqlWrapper.deleteDatabase("ChatterDB")


#Server variables.
client = ''
host = '127.0.0.1'
port = 500


#Class hold's individual chatter's info.
class Chatter:
    def __init__(self, name, primCol, secCol, authToken):
        self.primaryColor = primCol
        self.secondaryColor = secCol
        self.username = name
        self.authenticationToken = authToken
        self.isChatting = False
        self.chattingWith = None
    

#Class for primary server object that will handle all CRUD operations along with
#user conversations and accounts.
class ServerSession:
    def __init__(self):
        self.chattersOnlineList = []
    
    #Returns false if user is not in chattersOnlineList and returns the chatter if they are.
    def userOnline(self, username):


    #Generates a new 100 character session token for a user.
    def createSessionToken(self):
        newToken = ''.join(random.SystemRandom().choice(string.ascii_letters + string.digits) for _ in range(100))
        return newToken

    #Returns the authentication token if a log in is successful.
    def handleLogIn(self, username, password):
        if sqlWrapper.userExists(username) == True:
            userbuf = sqlWrapper.readUserData(username)
            if userbuf[1] == password:
                token = createSessionToken()
                self.chattersOnlineList.append( Chatter(usebuf[0], usebuf[2], usebuf[3], token) )
                return token
            else:
                return "Password is incorrect."
        else:
            return "User does not exist."

    #If name is taken return false, otherwise add a new user with default colors and return true.
    def addNewUser(self, username, password):
        if sqlWrapper.userExists(username) == False:
            sqlWrapper.addNewUser(username, password, "#FFFFFF", "#000000")
            return True
        else:
            return False

    #Returns true upon successful deletion of a user; false if user does not exist.
    def deleteUser(self, username):
        if sqlWrapper.userExists(username) == True:
            sqlWrapper.deleteUser(username)
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