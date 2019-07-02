import mysql.connector

connection = mysql.connector.connect(
  host="localhost",
  user="justin",
  passwd="password",
  database="Users_&_Passes"
)

cursor = connection.cursor()

class DatabaseAccessor():

    def selectUsername(self, username):
        cursor.execute("SELECT Username from Users WHERE Username = %s", (username,))
        selectedUsername = cursor.fetchone()
        return self.handleQueryReturn(selectedUsername)

    # selects user's hashed password based on username
    def selectHashedPassword(self, username):
        cursor.execute("SELECT HashedPass from Users WHERE Username = %s", (username,))
        selectedHashedPassword = cursor.fetchone()
        return self.handleQueryReturn(selectedHashedPassword)

    def selectUserId(self, userId):
        cursor.execute("SELECT UserId from Users WHERE UserId = %s", (userId,))
        selectedUserId = cursor.fetchone()
        return self.handleQueryReturn(selectedUserId)

    def insertUserInfo(self, username, hashedPassword, userId):
        cursor.execute("INSERT INTO Users(Username, HashedPass, UserId) VALUES(%s, %s, %s)", (username, hashedPassword, userId))
        connection.commit()
        username = ''
        hashedPassword = ''

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
