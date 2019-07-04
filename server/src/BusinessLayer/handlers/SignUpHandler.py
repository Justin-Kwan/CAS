import sys
sys.path.append('/Users/justinkwan/Documents/WebApps/UserAuth/server/src')
sys.path.append('/Users/justinkwan/Documents/WebApps/UserAuth/server/src/BusinessLayer/models')
sys.path.append('/Users/justinkwan/Documents/WebApps/UserAuth/server/src/DataBaseLayer')
from InputHandler     import InputHandler
from DatabaseAccessor import DatabaseAccessor
from ResultCodes      import ResultCodes
from User             import User
import uuid

inputHandler = InputHandler()
resultCodes  = ResultCodes()
DBA          = DatabaseAccessor()

class SignUpHandler():

    def handleUserSignUp(self, username, password):

        # check if inputs are null
        resultOfNullFieldCheck = inputHandler.checkInputNull(username, password)
        if resultOfNullFieldCheck != resultCodes.SUCCESS_FIELDS_FILLED:
            return resultOfNullFieldCheck

        user = self.getUser(str(username.lower()), str(password))

        # check if inputs are empty strings
        resultOfEmptyFieldCheck = inputHandler.handleEmptyInputFields(user)
        if resultOfEmptyFieldCheck != resultCodes.SUCCESS_FIELDS_FILLED:
            return resultOfEmptyFieldCheck

        # check for proper string input lengths
        resultOfInputLengthCheck = inputHandler.handleInputLengthChecks(user)
        if resultOfInputLengthCheck != resultCodes.SUCCESS_USERNAME_PASSWORD_LENGTH:
            return resultOfInputLengthCheck

        # check for invalid characters in inputs
        areUsernameCharsValid = inputHandler.verifyUsernameChars(user)
        if areUsernameCharsValid == False:
            return resultCodes.ERROR_INVALID_USERNAME_CHARS

        # check if username already exists
        doesUsernameExist = DBA.checkForExistingUsername(user)
        if doesUsernameExist:
            return resultCodes.ERROR_DUPLICATE_USERNAME

        # insert user info into db
        DBA.insertUserInfo(user)
        return resultCodes.SUCCESS

    def getUser(self, username, password):
        user = User(username, password)
        user.encryptAndUpdatePassword(password)
        user.generateAndUpdateUserId()
        return user
