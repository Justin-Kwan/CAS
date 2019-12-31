import sys
import os

THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
sys.path.append(THIS_FOLDER + '/../../DatabaseLayer')
sys.path.append(THIS_FOLDER + '/../../BusinessLayer/models')
sys.path.append(THIS_FOLDER + '/../../BusinessLayer')

from DatabaseAccessor import DatabaseAccessor
from User import User
from InputValidator import InputValidator
from TokenCheckHandler import TokenCheckHandler

DBA = DatabaseAccessor()
inputValidator = InputValidator()
tokenCheckHandler = TokenCheckHandler()

class PasswordResetHandler:

    def getJsonResponse(self, responseString, responseCode):
        return {
            'response string': responseString,
            'response code': responseCode
        }

    def handlePasswordReset(self, authToken, newTextPassword):
        response = tokenCheckHandler.handleTokenCheck(authToken)

        if not response['is user authorized']:
            return self.getJsonResponse('password reset unauthorized', 401)

        userid = response['user id']

        user = User(None, newTextPassword)
        user.setUserId(userid)

        passwordLengthCheck = inputValidator.checkInputLength(user, 'password')

        if passwordLengthCheck == 'password length bad':
            return self.getJsonResponse('password length bad', 402)

        user.encryptAndSetPassword()

        DBA.createConnection()
        DBA.updatePassword(user)
        DBA.closeConnection()
        
        return self.getJsonResponse('password reset successful', 205)
