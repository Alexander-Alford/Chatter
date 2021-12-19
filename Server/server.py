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
       # self.isChatting = False
        self.chattingWith = None
        self.timeToLive = 1800
    
class ChatRequest:
    def __init__(self, reqUser, recUser, reqToken, recToken):
        self.requester = reqUser
        self.receiver = recUser
        self.requestToken = reqToken
        self.receiveToken = recToken



#Class for primary server object that will handle all CRUD operations along with
#user conversations and accounts.
class ServerSession:
    def __init__(self):
        self.chattersOnlineList = []
        self.chatrequests = []
    
    #Returns false if user is not in chattersOnlineList and returns the chatter if they are.
    def userOnline(self, username):
        for chatter in self.chattersOnlineList:
            if chatter.username == username:
                return True
        return False

   # def userIsChatting(self, username):
     #   for chatter in self.chattersOnlineList:
     #       if chatter.isChatting == True:
     #           return True
     #   return False        

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
        x = -1
        for chatter in self.chattersOnlineList:
            x = x + 1
            if chatter.username == username:
                print("Username")
                if chatter.authenticationToken == token:
                    print("Authent")
                    print(x)
                    self.chattersOnlineList.pop(x)
                    print("Popped")
                    return True
                else:
                    return False
        return False

    #If name is taken return false, otherwise add a new user with default colors and return true.
    def addNewUser(self, username, password):
        if sqlWrapper.userExists(username) == False:
            sqlWrapper.addNewUser(username, password, "#FFFFFF", "#000000")
            return True
        else:
            print("Error making new user '%s'. User already exists."%username)
            return False

    #Returns true upon successful deletion of a user; otherwise an error message is returned.
    def deleteUser(self, username, token):
        if sqlWrapper.userExists(username) == True:
            if self.getUserToken(username) == token:
                sqlWrapper.deleteUser(username)
                sqlWrapper.deleteUserConversations(username)
                return True
            else:
                return "Error. Authentication failed."
        else:
            return "Error. User does not exist."
    
    def updateUserColors(self, username, token, priCol, secCol):
        if sqlWrapper.userExists(username) == True:
            if self.userOnline(username) == True:
                if self.getUserToken(username) == token:
                    if len(priCol) == 7 and len(secCol) == 7:
                        sqlWrapper.updatePrimaryColor(username, priCol)
                        sqlWrapper.updateSecondaryColor(username, secCol)
                        return True
                    else:
                        return "Error, bad color values."
                else:
                    return "Error, authentication failure."
            else:
                return "Error, user is not online."
        else:
            return "Error. User does not exist."

    #grabs a list of messages between two users at the request of one of them.
    def getChatConversation(self, requestUser, targetUser, reqUserToken):
        if sqlWrapper.userExists(requestUser) == True and sqlWrapper.userExists(targetUser) == True:
            if reqUserToken == self.getUserToken(requestUser):
                convo = sqlWrapper.readConversationLog(requestUser, targetUser)
                return convo
            else:
                return "Authentication failed."
        else:
            return "One of the users does not exist."

    #Uses auth token to get online user. Returns their name.
    def getUsernameBySessToken(self, token):
        index = -1
        for chatter in self.chattersOnlineList:
            index = index + 1
            if chatter.authenticationToken == token:
                return chatter.username
        return None
    
    def handleChatRequest(self, reqUser, reqToken, recUser):
        if self.userOnline(reqUser) == True or self.userOnline(recUser):
            if self.getUserToken(reqUser) == reqToken:
                for chatReq in self.chatrequests:
                    #If someone is looking to chat with reqUser and they are the receiving user of this call.
                    if chatReq.receiver == reqUser and chatReq.requester == recUser:
                        chatReq.receiveToken = reqToken
                        return "Chat between %s and %s started."%(recUser, reqUser)
                    #Change other chat request by same user if it exists and isn't an ongoing chat.
                    elif chatReq.requester == reqUser and chatReq.receiveToken = None:
                        chatReq.receiver = recUser
                        return "Chat invite by %s for another user has changed to be with %s"%(reqUser, recUser)
                #If no one is trying to chat with reqUser and he has no outgoing invites, add a new invite to the chatrequest list and return true.
                self.chatrequests.append( ChatRequest(reqUser, recUser, reqToken, None) )
                return True
            else:
                return "Error! User authentication failed."
        else:
            return "Error! Offline users cannot start chats."
    


    
#The primary server object that manages every online user and interacts with the database.
serverMain = ServerSession()

sqlWrapper.showTable("users")
sqlWrapper.showTable("chatlog")
    




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
            #print("HERE0")
            if serverMain.userOnline(req["Username"]) == True:
                #print("HERE1")
                if serverMain.handleLogOff(req["Username"], req["SessToken"]) == True:
                    detail = 'User successfully logged out.'
                    res = 'success'
                else:
                    detail = 'Authentication failed.'
                    res = 'failure'
            else:
                detail = 'User is not currently logged in.'
                res = 'failure'
        
        elif req["Selector"] == "DELETE":
            if serverMain.userOnline(req["Username"]) == True:
                #print("HERE")
                detail = serverMain.deleteUser(req["Username"], req["SessToken"])
                #print("HERE1")
                if detail == True:
                    #print("HERE2")
                    serverMain.handleLogOff(req["Username"], req["SessToken"])
                   # print("HERE3")
                    detail = "User successfully deleted."
                    res = "success"
                else:
                    res = "failure"
            else:
                detail = 'User must be logged in to delete account.'
                res = 'failure'
    
        return jsonify({'result':res, 'detail':detail})

    except:
        return "Error!"
    
@app.route('/api/account', methods=['PATCH'])
def handleColorUpdate():
    
    print('Hit on the account api.')

    req = request.json
    detail = 'null'
    res = 'null'

    try:
        detail = serverMain.updateUserColors(req["Username"], req["SessToken"], req["PrimaryColor"], req["SecondaryColor"])
        if detail == True:
            detail = "Colors updated to %s and %s"%(req["PrimaryColor"], req["SecondaryColor"])
            res = "success"
        else:
            res = "failure"
        return jsonify({'result':res, 'detail':detail})

    except:
        return "Error!"

@app.route('/api/chatroom', methods=['GET', 'POST'])
def manageChat():
    print('Hit on the chatroom api.')

    req = request.json
    res = 'null'
    dat = 'null'

    print(req)

    try:
        if req == None:
            chatterlist = []

            for chatter in serverMain.chattersOnlineList:
                chatterlist.append( {'name':str(chatter.username), 'primColor':str(chatter.primaryColor), 'secColor':str(chatter.secondaryColor), 'inChat':str(chatter.isChatting)} )
            dat = chatterlist
            res = "update"

        elif req["Selector"] == "CHATLOG":
            dat = serverMain.getChatConversation(req["reqUser"], req["targetUser"], req["SessToken"])
            if isinstance(dat, list):
                res = "success"
            else:
                res = "failure"
        
        

        return jsonify({'data':dat, 'result':res})

    except:
        return "Error!"

@app.route('/api/authcheck/<token>', methods=['GET'])
def checkAuthToken(token):
    print("Request to check auth token.")

    res = "failure"
    detail = "No user with auth token."
    name = serverMain.getUsernameBySessToken(token)

    if name != None:
        res = "success"
        detail = name

    print(res)
    return jsonify({'data':detail, 'result':res})

@app.route('/api/color/<username>', methods=['GET'])
def getColors(username):
    print("Request for colors.")

    userdata = sqlWrapper.readUserData



@app.route('/api/colorupdate', methods=['PATCH'])
def updateColors():
    print("Request to update colors.")
    
    req = request.json
    result = ""
    detail = serverMain.updateUserColors(req["Username"], req["SessToken"], req[""])






if __name__ == '__main__':
    app.run(host=host, port=port)