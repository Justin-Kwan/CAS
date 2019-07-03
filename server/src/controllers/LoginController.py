import sys
sys.path.append('/Users/justinkwan/Documents/WebApps/UserAuth/server/src')
from InputHandler     import InputHandler
from DatabaseAccessor import DatabaseAccessor
from ResultCodes      import ResultCodes
from User             import User

inputHandler = InputHandler()
resultCodes  = ResultCodes()
DBA          = DatabaseAccessor()

class LoginController():

    def handleUserLogin(self, username, password):

        # check if inputs are null
        fieldNullCheckResult = inputHandler.checkInputNull(username, password)
        if(fieldNullCheckResult != resultCodes.SUCCESS_FIELDS_FILLED):
            return fieldNullCheckResult

        user = self.getUser(str(username.lower()), str(password))

        # check if fields are empty strings
        fieldEmptyCheckResult = inputHandler.handleEmptyFields(user)
        if(fieldEmptyCheckResult != resultCodes.SUCCESS_FIELDS_FILLED):
            return fieldEmptyCheckResult

        # check if user exists
        doesUsernameExist = inputHandler.checkForExistingUsername(user)
        if(doesUsernameExist == False):
            return resultCodes.ERROR_INVALID_USERNAME_OR_PASSWORD

        # check if input password matches user's password
        isPasswordCorrect = inputHandler.verifyPassword(user)
        if(isPasswordCorrect == False):
            return resultCodes.ERROR_INVALID_USERNAME_OR_PASSWORD

        userId = DBA.selectUserId(user)
        user.updateUserId(userId)
        user.generateAndUpdateSecurityToken()
        securityToken = user.getSecurityToken()

        return securityToken

    def getUser(self, username, password):
        user = User(username, password)
        return user
