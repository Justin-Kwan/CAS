import mysql.connector

class DatabaseAccessor():

    def __init__(self):
        self.connection = None
        self.cursor = None

    def createConnection(self):
        self.connection = mysql.connector.connect(
            host="localhost",
            user="justin",
            passwd="password",
            database="Users_&_Passes"
        )
        self.cursor = self.connection.cursor()

    def selectUsername(self, user):
        username = user.getUsername()
        self.cursor.execute("SELECT Username from Users WHERE Username = %s", (username,))
        selectedUsername = self.cursor.fetchone()
        return self.handleQueryReturn(selectedUsername)

    def selectHashedPassword(self, user):
        username = user.getUsername()
        self.cursor.execute("SELECT HashedPass from Users WHERE Username = %s", (username,))
        selectedHashedPassword = self.cursor.fetchone()
        return self.handleQueryReturn(selectedHashedPassword)

    def selectUserId(self, user):
        username = user.getUsername()
        self.cursor.execute("SELECT UserId from Users WHERE Username = %s", (username,))
        selectedUserId = self.cursor.fetchone()
        return self.handleQueryReturn(selectedUserId)

    def insertUserInfo(self, user):
        username = user.getUsername()
        hashedPassword = user.getHashedPassword()
        userId = user.getUserId()
        self.cursor.execute("INSERT INTO Users(Username, HashedPass, UserId) VALUES(%s, %s, %s)", (username, hashedPassword, userId))
        self.connection.commit()

    def checkForExistingUsername(self, user):
        selectedUsername = self.selectUsername(user)
        doesUsernameExist = selectedUsername == user.getUsername()
        return doesUsernameExist

    def clearDatabase(self):
        self.cursor.execute('DELETE FROM Users')
        self.connection.commit()

    def closeConnection(self):
        self.cursor.close()
        self.connection.close()

    def handleQueryReturn(self, returnItem):
        try:
            return returnItem[0]
        # if no list item at index 0
        except:
            return None
