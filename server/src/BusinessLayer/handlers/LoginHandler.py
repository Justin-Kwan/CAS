import sys
sys.path.append('/Users/justinkwan/Documents/WebApps/UserAuth/server/src')
sys.path.append('/Users/justinkwan/Documents/WebApps/UserAuth/server/src/BusinessLayer/models')
sys.path.append('/Users/justinkwan/Documents/WebApps/UserAuth/server/src/DataBaseLayer')
from InputHandler     import InputHandler
from DatabaseAccessor import DatabaseAccessor
from ResultCodes      import ResultCodes
from User             import User

inputHandler = InputHandler()
resultCodes  = ResultCodes()
DBA          = DatabaseAccessor()

class LoginHandler():

    def handleUserLogin(self, username, password):

        # check if inputs are null
        resultOfNullFieldCheck = inputHandler.checkInputNull(username, password)
        if resultOfNullFieldCheck != resultCodes.SUCCESS_FIELDS_FILLED:
            return [resultCodes.NO_TOKEN, resultOfNullFieldCheck]

        user = self.getUser(str(username.lower()), str(password))

        # check if fields are empty strings
        resultOfEmptyFieldCheck = inputHandler.handleEmptyInputFields(user)
        if resultOfEmptyFieldCheck != resultCodes.SUCCESS_FIELDS_FILLED:
            return [resultCodes.NO_TOKEN, resultOfEmptyFieldCheck]

        # check if user exists
        doesUsernameExist = DBA.checkForExistingUsername(user)
        if doesUsernameExist == False:
            return [resultCodes.NO_TOKEN, resultCodes.ERROR_INVALID_USERNAME_OR_PASSWORD]

        # check if input password matches user's password
        selectedHashedPassword = DBA.selectHashedPassword(user).encode('utf-8')
        isPasswordCorrect = inputHandler.verifyPassword(user, selectedHashedPassword)
        if isPasswordCorrect == False:
            return [resultCodes.NO_TOKEN, resultCodes.ERROR_INVALID_USERNAME_OR_PASSWORD]

        userId = DBA.selectUserId(user)
        user.updateUserId(userId)
        user.generateAndUpdateSecurityToken()
        securityToken = user.getSecurityToken()

        return [securityToken, resultCodes.SUCCESS]

    def getUser(self, username, password):
        user = User(username, password)
        return user
