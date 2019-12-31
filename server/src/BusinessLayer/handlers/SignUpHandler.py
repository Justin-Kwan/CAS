import sys
import os

THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
sys.path.append(THIS_FOLDER + '/../../DatabaseLayer')
sys.path.append(THIS_FOLDER + '/../')
sys.path.append(THIS_FOLDER + '/../models')

from InputValidator   import InputValidator
from DatabaseAccessor import DatabaseAccessor
from User             import User
import uuid

inputValidator = InputValidator()
DBA            = DatabaseAccessor()

# HTTP Status Codes:
#   400 - Bad Signup Request (Bad Input)
#   201 - Created Signup
class SignUpHandler():

    def getJsonResponse(self, responseString, responseCode):
        return {
            'response string': responseString,
            'response code': responseCode
        }

    def handleUserSignUp(self, email, password):

        resultOfNullFieldCheck = inputValidator.checkInputNull(email, password)
        if resultOfNullFieldCheck != "email & password not null":
            return self.getJsonResponse(resultOfNullFieldCheck, 400)

        user = self.getUser(str(email.lower()), str(password))

        resultOfEmptyFieldCheck = inputValidator.checkInputEmpty(user)
        if resultOfEmptyFieldCheck != "email & password not empty":
            return self.getJsonResponse(resultOfEmptyFieldCheck, 400)

        resultOfInputLengthCheck = inputValidator.checkInputLength(user, 'email')
        if resultOfInputLengthCheck != "email length ok":
            return self.getJsonResponse(resultOfInputLengthCheck, 402)

        resultOfInputLengthCheck = inputValidator.checkInputLength(user, 'password')
        if resultOfInputLengthCheck != "password length ok":
            return self.getJsonResponse(resultOfInputLengthCheck, 402)

        isEmailCharsOk = inputValidator.isEmailCharsOk(user)
        if not isEmailCharsOk:
            return self.getJsonResponse("email invalid", 403)

        DBA.createConnection()

        doesEmailExist = DBA.doesEmailExist(user)
        if doesEmailExist:
            return self.getJsonResponse("email already exists", 404)

        DBA.insertUserInfo(user)
        DBA.closeConnection()
        return self.getJsonResponse("signup successful", 201)

    def getUser(self, email, textPassword):
        user = User(email, textPassword)
        user.encryptAndSetPassword()
        user.generateAndSetUserId()
        return user
