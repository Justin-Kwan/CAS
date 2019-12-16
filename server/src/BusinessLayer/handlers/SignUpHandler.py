import sys
sys.path.append('/Users/justinkwan/Documents/WebApps/UserAuth/server/src/BusinessLayer/models')
sys.path.append('/Users/justinkwan/Documents/WebApps/UserAuth/server/src/DataBaseLayer')
sys.path.append('/Users/justinkwan/Documents/WebApps/UserAuth/server/src/BusinessLayer')
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

    def handleUserSignUp(self, email, password):

        resultOfNullFieldCheck = inputValidator.checkInputNull(email, password)
        if resultOfNullFieldCheck != "email & password not null":
            return (resultOfNullFieldCheck, 400)

        user = self.getUser(str(email.lower()), str(password))

        resultOfEmptyFieldCheck = inputValidator.checkInputEmpty(user)
        if resultOfEmptyFieldCheck != "email & password not empty":
            return (resultOfEmptyFieldCheck, 400)

        resultOfInputLengthCheck = inputValidator.checkInputLength(user)
        if resultOfInputLengthCheck != "email & password length ok":
            return (resultOfInputLengthCheck, 402)

        isEmailCharsOk = inputValidator.isEmailCharsOk(user)
        if not isEmailCharsOk:
            return ("email invalid", 403)

        DBA.createConnection()

        doesEmailExist = DBA.checkForExistingEmail(user)
        if doesEmailExist:
            return ("email already exists", 404)

        DBA.insertUserInfo(user)
        DBA.closeConnection()
        return ("signup successful", 201)

    def getUser(self, email, password):
        user = User(email, password)
        user.encryptAndSetPassword(password)
        user.generateAndSetUserId()
        return user
