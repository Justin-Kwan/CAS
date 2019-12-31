import sys
import os

THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
sys.path.append(THIS_FOLDER + '/../.../DatabaseLayer')
sys.path.append(THIS_FOLDER + '/../')
sys.path.append(THIS_FOLDER + '/../models')

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

    def getJsonResponse(self, responseString, responseCode):
        return {
            'response string': responseString,
            'response code': responseCode
        }

    def handleUserLogin(self, email, password):

        resultOfNullFieldCheck = inputValidator.checkInputNull(email, password)
        if resultOfNullFieldCheck != "email & password not null":
            return self.getJsonResponse(resultOfNullFieldCheck, 400)

        user = User(str(email.lower()), str(password))

        resultOfEmptyFieldCheck = inputValidator.checkInputEmpty(user)
        if resultOfEmptyFieldCheck != "email & password not empty":
            return self.getJsonResponse(resultOfEmptyFieldCheck, 400)

        DBA.createConnection()

        doesEmailExist = DBA.doesEmailExist(user)
        if not doesEmailExist:
            return self.getJsonResponse("email or password wrong", 401)

        selectedHashedPassword = DBA.selectHashedPassword(user).encode('utf-8')
        isPasswordCorrect = inputValidator.isPasswordCorrect(user, selectedHashedPassword)
        if not isPasswordCorrect:
            return self.getJsonResponse("email or password wrong", 401)

        userId = DBA.selectUserIdFromEmail(user)
        DBA.closeConnection()

        user.setUserId(userId)
        user.generateAndSetAuthToken()
        authToken = user.getAuthToken()

        return self.getJsonResponse(authToken, 202)
