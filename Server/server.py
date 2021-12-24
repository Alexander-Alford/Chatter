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
        #self.chattingWith = None
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
                        for chatter in self.chattersOnlineList:
                            if chatter.username == username:
                                chatter.primaryColor = priCol
                                chatter.secondaryColor = secCol
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
    
    def setUserChatStatus(self, user, status):
        for chatter in self.chatterlist:
            if chatter.username == user:
                chatter.isChatting = status
                return

    #Creates a chat request for a user or matches them with the user they want to chat with.
    def handleChatRequest(self, reqUser, reqToken, recUser):
        #Make sure both users are online
        if self.userOnline(reqUser) == True and self.userOnline(recUser) == True:
            #Authenticate person trying to make the request
            if self.getUserToken(reqUser) == reqToken:
                for chatReq in self.chatrequests:
                    if chatReq.requester == recUser:
                        #Start a call if someone is looking to chat with the chat requester and they are the receiving user of the call.
                        if chatReq.receiver == reqUser:
                            chatReq.receiveToken = reqToken
                            self.setUserChatStatus(reqUser, True)
                            return (True, "Chat between %s and %s started."%(recUser, reqUser))
                        #Return a failure as the receiving user is already in a chat.
                        else:
                            return (False, "The receiving user %s is already in a chat with %s."%(recUser, chatReq.receiver))
                    #Change requesting user's preceding chat request if it exists and isn't an ongoing chat to requesting a different user.
                    elif chatReq.requester == reqUser and chatReq.receiveToken == None:
                        chatReq.receiver = recUser
                        return (True, "Chat invite by %s has changed to be with %s"%(reqUser, recUser))
                #No matching receiver with requester, no preceding requester invite, recieving user is not chatting.
                self.chatrequests.append( ChatRequest(reqUser, recUser, reqToken, None) )
                self.setUserChatStatus(reqUser, True)
                return (True, "Chat request for %s by %s created."%(recUser, reqUser))
            else:
                return (False, "Error! User authentication failed.")
        else:
            return (False, "Error! Offline users cannot start chats.")

    #Cancels a user's chat requests or ends the chat the requester is in.
    def cancelChatRequest(self, reqUser, reqToken):
        if self.getUserToken(reqUser) == reqToken:
            u = -1
            for chatReq in self.chatrequests:
                u = u + 1
                #Cancel chat/chat request if the requester is the requesting user. 
                if chatReq.requester == reqUser:
                    self.chatrequests.pop(u)
                    self.setUserChatStatus(reqUser, False)
                    #Set receiving user's chat status to false as the chat has ended.
                    if chatReq.receiveToken != None:
                        self.setUserChatStatus(chatReq.receiver, False)
                        return (True, "User %s's chat with %s has been ended."%(reqUser, chatReq.receiver))
                    return (True, "User %s's chat request has been canceled."%reqUser)
                #Cancel ongoing chat if the requesting user is a receiver and is currently in an active chat.
                elif chatReq.receiver == reqUser and chatReq.receiveToken != None:
                    self.chatrequests.pop(u)
                    self.setUserChatStatus(reqUser, False)
                    self.setUserChatStatus(chatReq.requester, False)
                    return (True, "User %s's chat with %s has ended at %s's request."%(chatReq.requester, reqUser, reqUser))

            return (False, "Error. User %s has no chat requests."%reqUser)
        else:
            return (False, "Error! User authentication failed.")
    

    def checkUserChatStatus(self, reqUser, reqToken):
        #Authenticate checking user.
        if self.getUserToken(reqUser) == reqToken:
            for chatReq in self.chatrequests:
                if chatReq.requester == reqUser:
                    if chatReq.receiveToken != None:
                        return ("chat", chatReq.receiver, "Chat between %s and %s."%(reqUser, chatReq.receiver))
                    else:
                        return ("request", chatReq.receiver, "Chat request by %s for %s."%(reqUser, chatReq.receiver))
                elif chatReq.receiver == reqUser:
                    if chatReq.receiveToken != None:
                        return ("chat", chatReq.requester, "Chat between %s and %s."%(reqUser, chatReq.requester))
                    else:
                        return ("requested", chatReq.requester, "Chat request by %s for %s."%(chatReq.requester, reqUser))
            
            return (False, None, "No chat/chat requests for %s have been started."%reqUser)    
        else:
            return (False, None, "Error! User authentication failed.")


    
#The primary server object that manages every online user and interacts with the database.
serverMain = ServerSession()

sqlWrapper.showTable("users")
sqlWrapper.showTable("chatlog")
    



#Route for logging in/out and creating/deleting accounts.
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
        
        elif req["Selector"] == "DELETE":
            if serverMain.userOnline(req["Username"]) == True:
                detail = serverMain.deleteUser(req["Username"], req["SessToken"])
                if detail == True:
                    serverMain.handleLogOff(req["Username"], req["SessToken"])
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

#Routing for updating user colors.    
@app.route('/api/account', methods=['PATCH'])
def handleColorUpdate():
    
    print('Hit on the account api.')

    req = request.json
    detail = 'null'
    res = 'null'

    
    try:
        username = serverMain.getUsernameBySessToken(req["SessToken"])
        detail = serverMain.updateUserColors(username, req["SessToken"], req["PrimaryColor"], req["SecondaryColor"])
        if detail == True:
            detail = "Colors updated to %s and %s"%(req["PrimaryColor"], req["SecondaryColor"])
            res = "success"
        else:
            res = "failure"
        return jsonify({'result':res, 'detail':detail})

    except:
        return "Error!"

#Routing for getting chatters online and getting conversation data.
@app.route('/api/chatroom', methods=['GET', 'POST'])
def manageChat():
    print('Hit on the chatroom api.')

    req = request.json
    res = 'null'
    dat = 'null'

    #print(req)

    try:
        if req == None:
            chatterlist = []
            for chatter in serverMain.chattersOnlineList:
                chatterlist.append( {'name':str(chatter.username), 'primColor':str(chatter.primaryColor), 'secColor':str(chatter.secondaryColor), 'inChat':str(chatter.isChatting)} )
            dat = chatterlist
            res = "update"
            print(dat)

        elif req["Selector"] == "CHATLOG":
            buf = serverMain.getChatConversation(req["reqUser"], req["targetUser"], req["SessToken"])
            if isinstance(buf, list):
                dat = []
                for message in buf:
                    dat.append( {'author':str(buf[0]) , 'content':str(buf[2]) , 'time':str(buf[3])} )
                res = "success"
            else:
                res = "failure"

        elif req["Selector"] == "CHATREQUEST":
            buf = serverMain.handleChatRequest(req["reqUser"], req["reqToken"], req["recUser"])
            dat = buf[1]
            res = "failure"
            if buf[0] == True:
                res = "success"

        elif req["Selector"] == "CHATREQCANCEL":
            buf = serverMain.cancelChatRequest(req["reqUser"], req["reqToken"])
            dat = buf[1]
            res = "failure"
            if buf[0] == True:
                res = "success"

        elif req["Selector"] == "CHATCHECK":
            buf = serverMain.checkUserChatStatus(req["reqUser"], req["reqToken"])
            dat = buf[1]
            
            res = "failure"
            if buf[0] == True:
                res = "success"
        

        return jsonify({'data':dat, 'result':res})

    except:
        return "Error!"

#Route for checking auth token on server.
@app.route('/api/authcheck/<token>', methods=['GET'])
def checkAuthToken(token):
    try:
        print("Request to check auth token.")

        res = "failure"
        detail = "No user with auth token."
        name = serverMain.getUsernameBySessToken(token)

        if name != None:
            res = "success"
            detail = name

        print(res)
        return jsonify({'data':detail, 'result':res})
    
    except:
        return "Error!"

#Route for getting client user color data.
@app.route('/api/color/<token>', methods=['GET'])
def getColors(token):
    try:
        print("Request for colors.")

        req = request.json
        res = "failure"

        username = serverMain.getUsernameBySessToken(token)

        if username != None:
            userdata = sqlWrapper.readUserData(username)
            res = "success"
            print(userdata)
            return jsonify({'pCol':userdata[2], 'sCol':userdata[3], 'result':res})
        else:
            return jsonify({'data':"Failure to get user colors.", 'result':res})

    except:
        return "Error!"        








if __name__ == '__main__':
    app.run(host=host, port=port)