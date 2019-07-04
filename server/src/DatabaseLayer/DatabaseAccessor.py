import mysql.connector

connection = mysql.connector.connect(
  host="localhost",
  user="justin",
  passwd="password",
  database="Users_&_Passes"
)

cursor = connection.cursor()

class DatabaseAccessor():

    def selectUsername(self, user):
        username = user.getUsername()
        cursor.execute("SELECT Username from Users WHERE Username = %s", (username,))
        selectedUsername = cursor.fetchone()
        return self.handleQueryReturn(selectedUsername)

    def selectHashedPassword(self, user):
        username = user.getUsername()
        cursor.execute("SELECT HashedPass from Users WHERE Username = %s", (username,))
        selectedHashedPassword = cursor.fetchone()
        return self.handleQueryReturn(selectedHashedPassword)

    def selectUserId(self, user):
        username = user.getUsername()
        cursor.execute("SELECT UserId from Users WHERE Username = %s", (username,))
        selectedUserId = cursor.fetchone()
        return self.handleQueryReturn(selectedUserId)

    def insertUserInfo(self, user):
        username = user.getUsername()
        hashedPassword = user.getHashedPassword()
        userId = user.getUserId()
        cursor.execute("INSERT INTO Users(Username, HashedPass, UserId) VALUES(%s, %s, %s)", (username, hashedPassword, userId))
        connection.commit()

    def checkForExistingUsername(self, user):
        selectedUsername = self.selectUsername(user)
        return selectedUsername == user.getUsername()

    def clearDatabase(self):
        cursor.execute('DELETE FROM Users')
        connection.commit()

    def closeConnection(self):
        cursor.close()
        connection.close()

    def handleQueryReturn(self, returnItem):
        try:
            return returnItem[0]
        except:
            return None
