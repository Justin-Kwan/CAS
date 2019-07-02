import sys
sys.path.append('/Users/justinkwan/Documents/WebApps/UserAuth/server/src')
from InputHandler     import InputHandler
from DatabaseAccessor import DatabaseAccessor
from ResultCodes      import ResultCodes
from User             import User


class LoginController():

    def handleUserLogin(self, username, password):

        user = self.getUser(str(username.lower()), str(password))

        # check if fields are empty
        fieldEmptyCheckResult = inputHandler.handleEmptyFields(user.getUsername(), user.getTextPassword())
        if(fieldEmptyCheckResult != resultCodes.SUCCESS_FIELDS_FILLED):
            return fieldEmptyCheckResult

        # check if user exists & check if input password matches user's password
        doesUsernameExist = inputHandler.checkForExistingUsername(user.getUsername())
        isPasswordCorrect = inputHandler.verifyPassword(user.getUsername(), user.getTextPassword())
        if(doesUsernameExist == False or isPasswordCorrect == False):
            return resultCodes.ERROR_INVALID_USERNAME_OR_PASSWORD

        # at this point, generate security token and return it
        #   - going to have user id problems



        user.generateAndUpdateSecurityToken()
        print(user.securityToken)



    def getUser(self, username, password):
        user = User(username, password)
        return user
