import sys
sys.path.append('/Users/justinkwan/Documents/WebApps/UserAuth/server/src')
sys.path.append('/Users/justinkwan/Documents/WebApps/UserAuth/server/src/BusinessLayer')
sys.path.append('/Users/justinkwan/Documents/WebApps/UserAuth/server/src/BusinessLayer/models')
sys.path.append('/Users/justinkwan/Documents/WebApps/UserAuth/server/src/DataBaseLayer')
from InputValidator   import InputValidator
from DatabaseAccessor import DatabaseAccessor
from ResultCodes      import ResultCodes
from User             import User

inputValidator = InputValidator()
resultCodes    = ResultCodes()
DBA            = DatabaseAccessor()

class LoginHandler():

    def handleUserLogin(self, username, password):

        # check if inputs are null
        resultOfNullFieldCheck = inputValidator.checkInputNull(username, password)
        if resultOfNullFieldCheck != resultCodes.SUCCESS_FIELDS_FILLED:
            return [resultCodes.NO_TOKEN, resultOfNullFieldCheck]

        user = self.getUser(str(username.lower()), str(password))

        # check if fields are empty strings
        resultOfEmptyFieldCheck = inputValidator.handleEmptyInputFields(user)
        if resultOfEmptyFieldCheck != resultCodes.SUCCESS_FIELDS_FILLED:
            return [resultCodes.NO_TOKEN, resultOfEmptyFieldCheck]

        DBA.createConnection()

        # check if user exists
        doesUsernameExist = DBA.checkForExistingUsername(user)
        if not doesUsernameExist:
            return [resultCodes.NO_TOKEN, resultCodes.ERROR_INVALID_USERNAME_OR_PASSWORD]

        # check if input password matches user's password
        selectedHashedPassword = DBA.selectHashedPassword(user).encode('utf-8')
        isPasswordCorrect = inputValidator.verifyPassword(user, selectedHashedPassword)
        if not isPasswordCorrect:
            return [resultCodes.NO_TOKEN, resultCodes.ERROR_INVALID_USERNAME_OR_PASSWORD]

        userId = DBA.selectUserId(user)
        DBA.closeConnection()

        user.setUserId(userId)
        user.generateAndSetAuthToken()
        authToken = user.getAuthToken()

        return [authToken, resultCodes.SUCCESS]

    def getUser(self, username, password):
        user = User(username, password)
        return user
