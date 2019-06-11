import sys
sys.path.append('/Users/justinkwan/Documents/WebApps/UserAuth/server/src')
from InputHandler     import InputHandler
from DatabaseAccessor import DatabaseAccessor
from ResultCodes      import ResultCodes

inputHandler     = InputHandler()
databaseAccessor = DatabaseAccessor()
resultCodes      = ResultCodes()

class SignUpController():

    def handleUserSignUp(self, username, password):

        username = str(username.lower())
        password = str(password)

        fieldEmptyCheckResult = inputHandler.handleEmptyFields(username, password)
        if(fieldEmptyCheckResult != resultCodes.SUCCESS_FIELDS_FILLED):
            return fieldEmptyCheckResult

        inputLengthResult = inputHandler.handleInputLengthChecks(username, password)
        if(inputLengthResult != resultCodes.SUCCESS_USERNAME_PASSWORD_LENGTH):
            return inputLengthResult

        isUsernameCharsValid = inputHandler.checkForInvalidUsernameChars(username)
        if(isUsernameCharsValid == False):
            return resultCodes.ERROR_INVALID_USERNAME_CHARS

        doesUsernameExist = inputHandler.checkForExistingUsername(username)
        if(doesUsernameExist):
            return resultCodes.ERROR_DUPLICATE_USERNAME

        hashedPassword = inputHandler.encryptPassword(password)
        databaseAccessor.insertUsernamePassword(username, hashedPassword)
        return resultCodes.SUCCESS
