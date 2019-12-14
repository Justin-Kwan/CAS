import sys
sys.path.append('/Users/justinkwan/Documents/WebApps/UserAuth/server/src/BusinessLayer')
sys.path.append('/Users/justinkwan/Documents/WebApps/UserAuth/server/src/BusinessLayer/models')
sys.path.append('/Users/justinkwan/Documents/WebApps/UserAuth/server/src/DataBaseLayer')
from InputValidator   import InputValidator
from DatabaseAccessor import DatabaseAccessor
from User             import User

inputValidator = InputValidator()
DBA            = DatabaseAccessor()

# HTTP Status Codes:
#   401 - Unauthorized Login
#   400 - Bad Login Request (Bad Input)
#   202 - Accpeted Login
class LoginHandler():

    def handleUserLogin(self, username, password):

        resultOfNullFieldCheck = inputValidator.checkInputNull(username, password)
        if resultOfNullFieldCheck != "username & password not null":
            return (resultOfNullFieldCheck, 400)

        user = self.getUser(str(username.lower()), str(password))

        resultOfEmptyFieldCheck = inputValidator.checkInputEmpty(user)
        if resultOfEmptyFieldCheck != "username & password not empty":
            return (resultOfEmptyFieldCheck, 400)

        DBA.createConnection()

        doesUsernameExist = DBA.checkForExistingUsername(user)
        if not doesUsernameExist:
            return ("username or password bad", 401)

        selectedHashedPassword = DBA.selectHashedPassword(user).encode('utf-8')
        isPasswordCorrect = inputValidator.isPasswordCorrect(user, selectedHashedPassword)
        if not isPasswordCorrect:
            return ("username or password bad", 401)

        userId = DBA.selectUserId(user)
        DBA.closeConnection()

        user.setUserId(userId)
        user.generateAndSetAuthToken()
        authToken = user.getAuthToken()

        return (authToken, 202)

    def getUser(self, username, password):
        user = User(username, password)
        return user
