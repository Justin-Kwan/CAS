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
        fieldNullCheck = inputHandler.checkInputNull(username, password)
        if fieldNullCheck != resultCodes.SUCCESS_FIELDS_FILLED:
            return fieldNullCheck

        user = self.getUser(str(username.lower()), str(password))

        # check if inputs are empty strings
        fieldEmptyCheck = inputHandler.handleEmptyFields(user)
        if fieldEmptyCheck != resultCodes.SUCCESS_FIELDS_FILLED:
            return fieldEmptyCheck

        # check for proper string input lengths
        inputLengthResult = inputHandler.handleInputLengthChecks(user)
        if inputLengthResult != resultCodes.SUCCESS_USERNAME_PASSWORD_LENGTH:
            return inputLengthResult

        # check for invalid characters in inputs
        isUsernameCharsValid = inputHandler.checkForInvalidUsernameChars(user)
        if isUsernameCharsValid == False:
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
