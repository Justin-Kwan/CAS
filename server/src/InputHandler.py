from UsernameHandler import UsernameHandler
from PasswordHandler import PasswordHandler
from DatabaseAccessor import DatabaseAccessor

usernameHandler = UsernameHandler()
passwordHandler = PasswordHandler()
databaseAccessor = DatabaseAccessor()

class InputHandler():

    ERROR_INVALID_USERNAME_CHARS = 'INVALID_USERNAME_CHARS'
    ERROR_DUPLICATE_USERNAME     = 'DUPLICATE_USERNAME'
    ERROR_EMPTY_USERNAME         = 'EMPTY_USERNAME'
    ERROR_EMPTY_PASSWORD         = 'EMPTY_PASSWORD'
    ERROR_EMPTY_FIELDS           = 'EMPTY_FIELDS'
    SUCCESS                      = 'SUCCESS'
    SUCCESS_FIELDS_FILLED        = 'ALL_FIELDS_FILLED'

    def handleUserInput(self, username, password):
        fieldEmptyCheckResult = self.handleEmptyFields(username, password)
        if(fieldEmptyCheckResult != self.SUCCESS_FIELDS_FILLED):
            return fieldEmptyCheckResult

        isUsernameCharsValid = usernameHandler.checkForInvalidUsernameChars(str(username))
        if(isUsernameCharsValid == False):
            return self.ERROR_INVALID_USERNAME_CHARS

        doesUsernameExist = usernameHandler.checkForExistingUsername(str(username))
        if(doesUsernameExist):
            return self.ERROR_DUPLICATE_USERNAME

        hashedPassword = passwordHandler.encryptPassword(str(password))
        databaseAccessor.insertUsernamePassword(username, hashedPassword)
        return self.SUCCESS

    def handleEmptyFields(self, username, password):
        isUsernameEmpty = self.checkTextEmpty(str(username))
        isPasswordEmpty = self.checkTextEmpty(str(password))

        if(isUsernameEmpty and isPasswordEmpty):
            return self.ERROR_EMPTY_FIELDS
        elif(isUsernameEmpty):
            return self.ERROR_EMPTY_USERNAME
        elif(isPasswordEmpty):
            return self.ERROR_EMPTY_PASSWORD
        else:
            return self.SUCCESS_FIELDS_FILLED

    def checkTextEmpty(self, text):
        if(text == ''):
            return True
        else:
            return False
