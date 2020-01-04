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
        self.cursor = self.connection.cursor(buffered = True)

    def selectEmail(self, user):
        email = user.getEmail()
        self.cursor.execute("SELECT Email from Users WHERE Email = %s", (email,))
        selectedEmail = self.cursor.fetchone()
        return self.handleQueryReturn(selectedEmail)

    def selectHashedPassword(self, user):
        email = user.getEmail()
        self.cursor.execute("SELECT HashedPass from Users WHERE Email = %s", (email,))
        selectedHashedPassword = self.cursor.fetchone()
        return self.handleQueryReturn(selectedHashedPassword)

    def selectUserIdFromEmail(self, user):
        email = user.getEmail()
        self.cursor.execute("SELECT UserId from Users WHERE Email = %s", (email,))
        selectedUserId = self.cursor.fetchone()
        return self.handleQueryReturn(selectedUserId)

    def selectUserId(self, user):
        userId = user.getUserId()
        self.cursor.execute("SELECT UserId from Users WHERE UserId = %s", (userId,))
        selectedUserId = self.cursor.fetchone()
        return self.handleQueryReturn(selectedUserId)

    def insertUserInfo(self, user):
        email = user.getEmail()
        hashedPassword = user.getHashedPassword()
        userId = user.getUserId()
        self.cursor.execute("INSERT INTO Users(Email, HashedPass, UserId) VALUES(%s, %s, %s)", (email, hashedPassword, userId))
        self.connection.commit()

    def updatePassword(self, user):
        userId = user.getUserId()
        hashedPassword = user.getHashedPassword()
        self.cursor.execute("UPDATE Users SET HashedPass = %s WHERE UserId = %s", (hashedPassword, userId))
        self.connection.commit()

    def doesEmailExist(self, user):
        selectedEmail = self.selectEmail(user)
        return selectedEmail == user.getEmail()

    def doesUserIdExist(self, user):
        selectedUserId = self.selectUserId(user)
        return selectedUserId == user.getUserId()

    def doesUserExist(self, user):
        doesUserExist = self.doesEmailExist(user) and self.doesUserIdExist(user)
        return doesUserExist

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
