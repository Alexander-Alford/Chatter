#Flask modules for http routing, requests, and responses.
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

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


#Wrapper class for all SQL functionality.
class SQL_Wrapper:
    def addNewUser(username, password):
        pass
    def deleteUser(username):
        pass
    def checkUserExists(username):
        pass
    def checkPassword(password):
        pass
    

    


    




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