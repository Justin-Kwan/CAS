import sys
sys.path.append('/Users/justinkwan/Documents/WebApps/UserAuth/server/src')
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
        fieldNullCheckResult = inputHandler.checkInputNull(username, password)
        if fieldNullCheckResult != resultCodes.SUCCESS_FIELDS_FILLED:
            return fieldNullCheckResult

        user = self.getUser(str(username.lower()), str(password))

        # check if inputs are empty strings
        fieldEmptyCheckResult = inputHandler.handleEmptyFields(user)
        if fieldEmptyCheckResult != resultCodes.SUCCESS_FIELDS_FILLED:
            return fieldEmptyCheckResult

        # check for proper string input lengths
        inputLengthResult = inputHandler.handleInputLengthChecks(user)
        if inputLengthResult != resultCodes.SUCCESS_USERNAME_PASSWORD_LENGTH:
            return inputLengthResult

        # check for invalid characters in inputs
        isUsernameCharsValid = inputHandler.checkForInvalidUsernameChars(user)
        if isUsernameCharsValid == False:
            return resultCodes.ERROR_INVALID_USERNAME_CHARS

        # check if username already exists
        doesUsernameExist = inputHandler.checkForExistingUsername(user)
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
