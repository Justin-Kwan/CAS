import sys
sys.path.append('/Users/justinkwan/Documents/WebApps/UserAuth/server/src')
import bcrypt
from validate_email import validate_email

class InputValidator():

    def checkInputNull(self, email, password):
        if email is None:
            return "email null"
        if password is None:
            return "password null"
        return "email & password not null"

    def checkInputEmpty(self, user):
        email = user.getEmail()
        password = user.getTextPassword()

        if len(email) == 0:
            return "email empty"
        elif len(password) == 0:
            return "password empty"
        return "email & password not empty"

    def checkInputLength(self, user):
        email = user.getEmail()
        password = user.getTextPassword()

        isEmailLengthOk = len(email) >= 7 and len(email) <= 89
        isPasswordLengthOk = len(password) >= 8 and len(password) <= 65

        if not isEmailLengthOk:
            return "email length bad"
        if not isPasswordLengthOk:
            return "password length bad"
        return "email & password length ok"

    def isEmailCharsOk(self, user):
        email = user.getEmail()
        isEmailCharsOk = validate_email(email)

        return isEmailCharsOk


    def isPasswordCorrect(self, user, selectedHashedPassword):
        password = user.getTextPassword().encode('utf-8')
        isPasswordCorrect = bcrypt.checkpw(password, selectedHashedPassword) == True

        return isPasswordCorrect
