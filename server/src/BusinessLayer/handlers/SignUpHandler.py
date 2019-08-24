import sys
sys.path.append('/Users/justinkwan/Documents/WebApps/UserAuth/server/src')
sys.path.append('/Users/justinkwan/Documents/WebApps/UserAuth/server/src/BusinessLayer/models')
sys.path.append('/Users/justinkwan/Documents/WebApps/UserAuth/server/src/DataBaseLayer')
sys.path.append('/Users/justinkwan/Documents/WebApps/UserAuth/server/src/BusinessLayer')
from InputValidator   import InputValidator
from DatabaseAccessor import DatabaseAccessor
from ResultCodes      import ResultCodes
from User             import User
import uuid

inputValidator = InputValidator()
resultCodes    = ResultCodes()
DBA            = DatabaseAccessor()

class SignUpHandler():

    def handleUserSignUp(self, username, password):

        # check if inputs are null
        resultOfNullFieldCheck = inputValidator.checkInputNull(username, password)
        if resultOfNullFieldCheck != resultCodes.SUCCESS_FIELDS_FILLED:
            return resultOfNullFieldCheck

        user = self.getUser(str(username.lower()), str(password))

        # check if inputs are empty strings
        resultOfEmptyFieldCheck = inputValidator.handleEmptyInputFields(user)
        if resultOfEmptyFieldCheck != resultCodes.SUCCESS_FIELDS_FILLED:
            return resultOfEmptyFieldCheck

        # check for proper string input lengths
        resultOfInputLengthCheck = inputValidator.handleInputLengthChecks(user)
        if resultOfInputLengthCheck != resultCodes.SUCCESS_USERNAME_PASSWORD_LENGTH:
            return resultOfInputLengthCheck

        # check for invalid characters in inputs
        areUsernameCharsValid = inputValidator.verifyUsernameChars(user)
        if not areUsernameCharsValid:
            return resultCodes.ERROR_INVALID_USERNAME_CHARS

        DBA.createConnection()

        # check if username already exists
        doesUsernameExist = DBA.checkForExistingUsername(user)
        if doesUsernameExist:
            return resultCodes.ERROR_DUPLICATE_USERNAME

        # insert user info into db
        DBA.insertUserInfo(user)
        DBA.closeConnection()
        return resultCodes.SUCCESS

    def getUser(self, username, password):
        user = User(username, password)
        user.encryptAndSetPassword(password)
        user.generateAndSetUserId()
        return user
