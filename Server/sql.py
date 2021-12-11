


#Wrapper class for all SQL functionality.
class SQL_Wrapper:
    
    def DatabaseExists(db_name):
        Cursor.execute("SHOW DATABASES")
        db_list = [ x[0] for x in Cursor.fetchall() ]
        if db_name in db_list:
            return True
        else:
            return False

    def TableExists(table_name):
        Cursor.execute("SHOW TABLES")
        table_list = [ x[0] for x in Cursor.fetchall() ]
        if table_name in table_list:
            return True
        else:
            return False

    def addNewUser(username, password):
        pass
    def deleteUser(username):
        pass
    def checkUserExists(username):
        pass
    def checkPassword(password):
        pass
    def connectToSQLDatabase():
        pass