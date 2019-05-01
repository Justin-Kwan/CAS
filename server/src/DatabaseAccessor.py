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
        return selectedUsername

    def selectPassword(self, hashedPassword):
        cursor.execute("SELECT HashedPass from Users WHERE HashedPass = %s", (hashedPassword,))
        selectedPassword = cursor.fetchone()
        return selectedPassword

    def insertUsernamePassword(self, username, hashedPassword):
        cursor.execute("INSERT INTO Users(Username, HashedPass) VALUES(%s, %s)", (username, hashedPassword))
        connection.commit()
        uername = ''
        hashedPassword = ''

    def clearDatabase(self):
        cursor.execute('DELETE FROM Users')
        connection.commit()

    def closeConnection(self):
        cursor.close()
        connection.close()
