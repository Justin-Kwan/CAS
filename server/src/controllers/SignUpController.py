import sys
sys.path.append('/Users/justinkwan/Documents/WebApps/UserAuth/server/src')
from InputHandler     import InputHandler
from DatabaseAccessor import DatabaseAccessor
from ResultCodes      import ResultCodes
from User             import User
import uuid

inputHandler     = InputHandler()
DBA = DatabaseAccessor()
resultCodes      = ResultCodes()

class SignUpController():

    def handleUserSignUp(self, username, password):

        user = self.getUser(str(username.lower()), str(password))

        # # check if fields are empty
        # fieldEmptyCheckResult = inputHandler.handleEmptyFields(user.getUsername(), user.getTextPassword())
        # if(fieldEmptyCheckResult != resultCodes.SUCCESS_FIELDS_FILLED):
        #     return fieldEmptyCheckResult

        # pass user
        fieldEmptyCheckResult = inputHandler.handleEmptyFields(user)
        if(fieldEmptyCheckResult != resultCodes.SUCCESS_FIELDS_FILLED):
            return fieldEmptyCheckResult


        # check for proper string input lengths
        inputLengthResult = inputHandler.handleInputLengthChecks(user.getUsername(), user.getTextPassword())
        if(inputLengthResult != resultCodes.SUCCESS_USERNAME_PASSWORD_LENGTH):
            return inputLengthResult

        # check for invalid characters in inputs
        isUsernameCharsValid = inputHandler.checkForInvalidUsernameChars(user.getUsername())
        if(isUsernameCharsValid == False):
            return resultCodes.ERROR_INVALID_USERNAME_CHARS

        # check if username already exists
        doesUsernameExist = inputHandler.checkForExistingUsername(user.getUsername())
        if(doesUsernameExist):
            return resultCodes.ERROR_DUPLICATE_USERNAME

        # insert user info into db
        DBA.insertUserInfo(user.getUsername(), user.getHashedPassword(), user.getUserId())
        return resultCodes.SUCCESS

    def getUser(self, username, password):
        user = User(username, password)
        user.encryptAndUpdatePassword(password)
        return user
