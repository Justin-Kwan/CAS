import os
import sys

THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
sys.path.append(THIS_FOLDER + '/../src/DatabaseLayer')
sys.path.append(THIS_FOLDER + '/../src/BusinessLayer')
sys.path.append(THIS_FOLDER + '/../src/BusinessLayer/models')

from TokenChecker import TokenChecker
from DatabaseAccessor import DatabaseAccessor
from User import User

DBA = DatabaseAccessor()

class TokenCheckHandler:

    def __init__(self):
        self.tokenChecker = TokenChecker()

    def getJsonResponse(self, isUserAuthorized, userId, responseCode):
        return {
            'is user authorized': isUserAuthorized,
            'user id': userId,
            'response code': responseCode
        }

    def handleTokenCheck(self, authToken):
        tokenPayload = self.tokenChecker.getTokenPayload(str(authToken))

        if tokenPayload == False:
            return self.getJsonResponse(False, 'unauthorized', 401)

        email = str(tokenPayload['email'])
        userId = str(tokenPayload['user id'])

        user = User(email, None)
        user.setUserId(userId)
        user.setAuthToken(str(authToken))

        DBA.createConnection()
        doesUserExist = DBA.doesUserExist(user)
        DBA.closeConnection()

        if not doesUserExist:
            return self.getJsonResponse(False, 'unauthorized', 401)

        return self.getJsonResponse(True, user.getUserId(), 200)
