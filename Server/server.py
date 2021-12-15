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
        self.timeToLive = 1800
    

#Class for primary server object that will handle all CRUD operations along with
#user conversations and accounts.
class ServerSession:
    def __init__(self):
        self.chattersOnlineList = []
    
    #Returns false if user is not in chattersOnlineList and returns the chatter if they are.
    def userOnline(self, username):
        for chatter in self.chattersOnlineList:
            if chatter.username == username:
                return True
        return False
            

    #Generates a new 100 character session token for a user.
    def createSessionToken(self):
        newToken = ''.join(random.SystemRandom().choice(string.ascii_letters + string.digits) for _ in range(100))
        return newToken
    
    def getUserToken(self, username):
        for chatter in self.chattersOnlineList:
            if chatter.username == username:
                return chatter.authenticationToken
        return None


    #Returns the authentication token if a log in is successful.
    def handleLogIn(self, username, password):
        if sqlWrapper.userExists(username) == True:
            userbuf = sqlWrapper.readUserData(username)
            if userbuf[1] == password:
                print(userbuf)
                token = self.createSessionToken()
                self.chattersOnlineList.append( Chatter(userbuf[0], userbuf[2], userbuf[3], token) )
                return token
            else:
                return "Password is incorrect."
        else:
            return "User does not exist."

    def handleLogOff(self, username, token):
        print("Log off for %s"%username)
        for chatter in self.chattersOnlineList:
            if chatter.username == username:
                print("Username")
                if chatter.authenticationToken == token:
                    print("Authent")
                    self.chattersOnlineList.pop(index(chatter))
                    print("Popped")
                    return True
                else:
                    return False

    #If name is taken return false, otherwise add a new user with default colors and return true.
    def addNewUser(self, username, password):
        if sqlWrapper.userExists(username) == False:
            sqlWrapper.addNewUser(username, password, "#FFFFFF", "#000000")
            return True
        else:
            print("Error making new user '%s'. User already exists."%username)
            return False

    #Returns true upon successful deletion of a user; false if user does not exist.
    def deleteUser(self, username):
        if sqlWrapper.userExists(username) == True:
            sqlWrapper.deleteUser(username)
            return True
        else:
            return False
    

serverMain = ServerSession()


    




@app.route('/api/signin', methods=['POST', 'DELETE'])
def handleSignInRoute():
    try:
        print('POST on the sign-in api.')
        req = request.json
        detail = 'null'
        res = 'null'
    
        if req["Selector"] == "LOGIN":
            #print("Login request.")
            if serverMain.userOnline(req["Username"]) != True:
                detail = serverMain.handleLogIn(req["Username"], req["Password"])
                if len(detail) == 100:
                    res = 'success'
                else:
                    res = 'failure'
                    
            else:
                detail = 'Account is already logged in on another computer.'
                res = 'failure'

        elif req["Selector"] == "MAKE":
            #print("Make request.")
            if serverMain.addNewUser(req["Username"], req["Password"]) == True:
                detail = 'User created successfully.'
                res = 'success'
            else:
                detail = 'Username is already in use.'
                res = 'failure'

        elif req["Selector"] == "LOGOUT":
            if serverMain.userOnline(req["Username"]) == True:
                if serverMain.handleLogOff(req["Username"], req["SessToken"]) == True:
                    detail = 'User successfully logged out.'
                    res = 'success'
                else:
                    detail = 'Authentication failed.'
                    res = 'failure'
            else:
                detail = 'User is not currently logged in.'
                res = 'failure'
    
        return jsonify({'result':res, 'detail':detail})

    except:
        return "Error!"
    
@app.route('/api/account', methods=['PATCH'])
def handleColorUpdate():
    print('Hit on the account api.')
    return "Color!"

@app.route('/api/chatroom', methods=['GET', 'POST'])
def manageChat():
    print('Hit on the chat room api.')
    return "Hello World!"



if __name__ == '__main__':
    app.run(host=host, port=port)