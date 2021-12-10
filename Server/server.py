#Modules for handling environment variables.
import os
from dotenv import load_dotenv
#Flask modules for http routing, requests, and responses.
from flask import Flask, jsonify, request
from flask_cors import CORS

import boto3




app = Flask(__name__)
CORS(app)
load_dotenv()

#AWS database environment variables.
DB_NAME = os.environ.get("AWS_DBNAME")
DB_ENDPOINT = os.environ.get("AWS_ENDPOINT")
DB_PORT = os.environ.get("AWS_PORT")
DB_REGION = os.environ.get("AWS_REGION")
DB_USERNAME = os.environ.get("AWS_USER")
DB_PASSWORD = os.environ.get("")


os.environ['LIBMYSQL_ENABLE_CLEARTEXT_PLUGIN'] = '1'

#gets the credentials from .aws/credentials
session = boto3.Session()
client = session.client()

token = client.generate_db_auth_token(DBHostname=DB_ENDPOINT, Port=DB_PORT, DBUsername=DB_USERNAME, Region=DB_REGION) 



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