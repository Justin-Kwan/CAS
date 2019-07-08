import sys
sys.path.append('/Users/justinkwan/Documents/WebApps/UserAuth/server/src')
from ResultCodes import ResultCodes
import bcrypt

resultCodes = ResultCodes()

class InputValidator():

    def checkInputNull(self, username, password):
        USERNAME_AND_PASSWORD_NULL        = username == None and password == None
        USERNAME_NULL_AND_PASSWORD_FILLED = username == None and password != None
        USERNAME_FILLED_AND_PASSWORD_NULL = username != None and password == None

        if USERNAME_AND_PASSWORD_NULL:
            return resultCodes.ERROR_EMPTY_FIELDS
        elif USERNAME_NULL_AND_PASSWORD_FILLED:
            return resultCodes.ERROR_EMPTY_USERNAME
        elif USERNAME_FILLED_AND_PASSWORD_NULL:
            return resultCodes.ERROR_EMPTY_PASSWORD
        else:
            return resultCodes.SUCCESS_FIELDS_FILLED

    def handleEmptyInputFields(self, user):
        username = user.getUsername()
        password = user.getTextPassword()

        isUsernameEmpty = self.checkInputEmpty(username)
        isPasswordEmpty = self.checkInputEmpty(password)

        if isUsernameEmpty and isPasswordEmpty:
            return resultCodes.ERROR_EMPTY_FIELDS
        elif isUsernameEmpty:
            return resultCodes.ERROR_EMPTY_USERNAME
        elif isPasswordEmpty:
            return resultCodes.ERROR_EMPTY_PASSWORD
        else:
            return resultCodes.SUCCESS_FIELDS_FILLED

    def checkInputEmpty(self, text):
        TEXT_EMPTY = len(text) == 0

        if TEXT_EMPTY:
            return True
        return False

    def handleInputLengthChecks(self, user):
        username = user.getUsername()
        password = user.getTextPassword()

        isUsernameLengthOk = self.verifyInputLength('USERNAME', username)
        isPasswordLengthOk = self.verifyInputLength('PASSWORD', password)

        if isUsernameLengthOk and isPasswordLengthOk:
            return resultCodes.SUCCESS_USERNAME_PASSWORD_LENGTH
        elif not isUsernameLengthOk and isPasswordLengthOk:
            return resultCodes.ERROR_USERNAME_LENGTH_INVALID
        elif isUsernameLengthOk and not isPasswordLengthOk:
            return resultCodes.ERROR_PASSWORD_LENGTH_INVALID
        else:
            return resultCodes.ERROR_USERNAME_LENGTH_INVALID

    def verifyInputLength(self, inputType, input):
        if inputType == 'USERNAME':
            return len(input) >= 6 and len(input) <= 35
        elif inputType == 'PASSWORD':
            return len(input) >= 8 and len(input) <= 65

    def verifyUsernameChars(self, user):
        username = user.getUsername()

        for currentChar in username:
            if not currentChar.isalpha() and not currentChar.isdigit():
                return False
        return True

    def verifyPassword(self, user, selectedHashedPassword):
        password = user.getTextPassword().encode('utf-8')
        PASSWORD_CORRECT = bcrypt.checkpw(password, selectedHashedPassword) == True

        if PASSWORD_CORRECT:
            return True
        else:
            return False
