import sys
sys.path.append('/Users/justinkwan/Documents/WebApps/UserAuth/server/src')
import bcrypt

class InputValidator():

    def checkInputNull(self, username, password):
        if username is None:
            return "username null"
        if password is None:
            return "password null"
        return "username & password not null"

    def checkInputEmpty(self, user):
        username = user.getUsername()
        password = user.getTextPassword()

        if len(username) == 0:
            return "username empty"
        elif len(password) == 0:
            return "password empty"
        return "username & password not empty"

    def checkInputLength(self, user):
        username = user.getUsername()
        password = user.getTextPassword()

        isUsernameLengthOk = len(username) >= 6 and len(username) <= 35
        isPasswordLengthOk = len(password) >= 8 and len(password) <= 65

        if not isUsernameLengthOk:
            return "username length bad"
        if not isPasswordLengthOk:
            return "password length bad"
        return "username & password length ok"

    def isUsernameCharsOk(self, user):
        username = user.getUsername()
        isUsernameCharsOk = username.isalnum()

        return isUsernameCharsOk

    def isPasswordCorrect(self, user, selectedHashedPassword):
        password = user.getTextPassword().encode('utf-8')
        isPasswordCorrect = bcrypt.checkpw(password, selectedHashedPassword) == True

        return isPasswordCorrect
