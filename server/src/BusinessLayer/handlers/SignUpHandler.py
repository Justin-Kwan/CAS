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

    def handleUserSignUp(self, username, password):

        resultOfNullFieldCheck = inputValidator.checkInputNull(username, password)
        if resultOfNullFieldCheck != "username & password not null":
            return (resultOfNullFieldCheck, 400)

        user = self.getUser(str(username.lower()), str(password))

        resultOfEmptyFieldCheck = inputValidator.checkInputEmpty(user)
        if resultOfEmptyFieldCheck != "username & password not empty":
            return (resultOfEmptyFieldCheck, 400)

        resultOfInputLengthCheck = inputValidator.checkInputLength(user)
        if resultOfInputLengthCheck != "username & password length ok":
            return (resultOfInputLengthCheck, 400)

        isUsernameCharsOk = inputValidator.isUsernameCharsOk(user)
        if not isUsernameCharsOk:
            return ("username characters bad", 400)

        DBA.createConnection()

        doesUsernameExist = DBA.checkForExistingUsername(user)
        if doesUsernameExist:
            return ("username already exists", 400)

        DBA.insertUserInfo(user)
        DBA.closeConnection()
        return ("signup successful", 201)

    def getUser(self, username, password):
        user = User(username, password)
        user.encryptAndSetPassword(password)
        user.generateAndSetUserId()
        return user
