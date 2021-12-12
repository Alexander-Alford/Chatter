#Module for MySQL funcionality.
import mysql.connector


#Wrapper class for all SQL functionality.
class SQL_Wrapper:
    
    def __init__(self, host, user, password):
        self.sql_database = mysql.connector.connect(
              host=host,
              user=user,
              password=password
            )
        
        self.Cursor = self.sql_database.cursor()
        #self.CursorBuffer = NULL

        try:
            self.Cursor.execute("CREATE DATABASE ChatterDB")
            print("ChatterDB database created.")
        except:
            print("ChatterDB database already exists.")
        
        self.sql_database = mysql.connector.connect(
              host=host,
              user=user,
              password=password,
              database="ChatterDB"
            )
        
        self.Cursor = self.sql_database.cursor()

        try:
            self.Cursor.execute("CREATE TABLE users (username VARCHAR(50) NOT NULL, password VARCHAR(50) NOT NULL, primarycolor CHAR(7), secondarycolor CHAR(7), PRIMARY KEY(username))")
            print("users table created.")
        except:
            print("users table already exists.")
        
        try:
            self.Cursor.execute("CREATE TABLE chatlog (sender VARCHAR(50) NOT NULL, receiver VARCHAR(50) NOT NULL, content TINYTEXT NOT NULL, timestamp INT UNSIGNED NOT NULL)")
            print("chatlog table created.")
        except:
            print("chatlog table already exists.")



    def DatabaseExists(self, db_name):
        self.Cursor.execute("SHOW DATABASES")
        db_list = [ x[0] for x in self.Cursor.fetchall() ]
        if db_name in db_list:
            return True
        else:
            return False

    def TableExists(self, table_name):
        self.Cursor.execute("SHOW TABLES")
        table_list = [ x[0] for x in self.Cursor.fetchall() ]
        if table_name in table_list:
            return True
        else:
            return False

    def addNewUser(self, username, password, primCol, seconCol):
        try:
            sql = "INSERT INTO users (username, password, primarycolor, secondarycolor) VALUES (%s, %s, %s, %s)"
            val = (username, password, primCol, seconCol)
            self.Cursor.execute(sql, val)
            self.sql_database.commit()
            print("User '%s' added."%username)
        except:
            print("Error! User not created. Username '%s' is already taken."%username)

    def deleteUser(self, username):
        try:
            sql = "DELETE FROM users WHERE username = %s"
            adr = (username, )
            self.Cursor.execute(sql, adr)
            self.sql_database.commit()
            print("User '%s' was deleted."%username)
        except: 
            print("Could not delete user. User '%s' does not exist."%username)

    def showTable(self, table_name):
        try:
            self.Cursor.execute("SELECT * FROM %s"%table_name)

            buf = self.Cursor.fetchall()

            for x in buf:
              print(x)
        except:
            print("Table '%s' does not exist."%table_name)

    def deleteDatabase(self, database):
        try:
            self.Cursor.execute("DROP DATABASE %s"%database)
            print("Database '%s' deleted."%database)
        except:
            print("Database '%s' does not exist."%database)

    def addChatMessage(self, sender, receiver, content, timestamp):
        try:
            sql = "INSERT INTO chatlog (sender, receiver, content, timestamp) VALUES (%s, %s, %s, %s)"
            val = (sender, receiver, content, timestamp)
            self.Cursor.execute(sql, val)
            self.sql_database.commit()
            print("Message sent from %s to %s."%(sender, receiver))
        except:
            print("Error processing message from %s to %s"%(sender, receiver))

    def deleteUserConversations(self, username):
        try:
            sql ="""DELETE  
                    FROM chatlog
                    WHERE sender = %s 
                    OR receiver = %s"""
            val = (username, username)

            self.Cursor.execute(sql, val)
            self.sql_database.commit()

            print("User %s's conversation has been deleted."%username)
        except:
            print("Error! Conversation does not exist.")

    def readUserData(self, username):
        try:
            sql = "SELECT * FROM users WHERE username = %s"
            self.Cursor.execute(sql, (username,))
            buf = self.Cursor.fetchone() 
            return buf
        except:
            print("Error. User %s does not exist."%username)
            return None

    def readConversationLog(self, userOne, userTwo):
        try:
            sql ="""SELECT *
                    FROM chatlog
                    WHERE (sender = %s AND receiver = %s) OR (sender = %s AND receiver = %s)
                    ORDER BY timestamp ASC
                    """
            val = (userOne, userTwo, userTwo, userOne)
            self.Cursor.execute(sql, val)
            buf = self.Cursor.fetchall()
            return buf
        except:
            print("Error. Could not read conversation between %s and %s."%(userOne, userTwo))
            return None

    def updatePrimaryColor(self, username, newcolor):
        try:
        except:
            print("Could not update colors ")
            return None