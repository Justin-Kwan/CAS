import re
import bcrypt
from validate_email import validate_email

class InputValidator():

    def __init__(self):
        self.emailRegex = '''(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\\.[a-z0-9!#$%&'*+/=?
                             ^_`{|}~-]+)*|"(?:[\\x01-\\x08\\x0b\\x0c\\x0e-\\x1f\\x21
                             \\x23-\\x5b\\x5d-\\x7f]|\\\\[\\x01-\\x09\\x0b\\x0c\\x0e
                             -\\x7f])*")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\\.)+[
                             a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\\[(?:(?:25[0-5]|2[0-4][
                             0-9]|[01]?[0-9][0-9]?)\\.){3}(?:25[0-5]|2[0-4][0-9]|[01
                             ]?[0-9][0-9]?|[a-z0-9-]*[a-z0-9]:(?:[\\x01-\\x08\\x0b\\
                             x0c\\x0e-\\x1f\\x21-\\x5a\\x53-\\x7f]|\\\\[\\x01-\\x09\
                             \x0b\\x0c\\x0e-\\x7f])+)\\])'''

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

    def checkInputLength(self, user, inputType):
        if inputType == 'email':
            email = user.getEmail()
            isEmailLengthOk = len(email) >= 7 and len(email) <= 89

            if not isEmailLengthOk:
                return "email length bad"
            else:
                return 'email length ok'

        if inputType == 'password':
            password = user.getTextPassword()
            isPasswordLengthOk = len(password) >= 8 and len(password) <= 65

            if not isPasswordLengthOk:
                return "password length bad"
            else:
                return 'password length ok'

    def isEmailCharsOk(self, user):
        email = user.getEmail()
        match = re.match(self.emailRegex, email)

        if match == None:
	        return False
        else:
            return True

    def isPasswordCorrect(self, user, selectedHashedPassword):
        password = user.getTextPassword().encode('utf-8')
        isPasswordCorrect = bcrypt.checkpw(password, selectedHashedPassword) == True
        return isPasswordCorrect
