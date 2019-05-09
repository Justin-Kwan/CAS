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

        username = str(username.lower())
        password = str(password)

        fieldEmptyCheckResult = self.handleEmptyFields(username, password)
        if(fieldEmptyCheckResult != self.SUCCESS_FIELDS_FILLED):
            return fieldEmptyCheckResult

        '''check for char count of inputs'''

        isUsernameCharsValid = usernameHandler.checkForInvalidUsernameChars(username)
        if(isUsernameCharsValid == False):
            return self.ERROR_INVALID_USERNAME_CHARS

        doesUsernameExist = usernameHandler.checkForExistingUsername(username)
        if(doesUsernameExist):
            return self.ERROR_DUPLICATE_USERNAME

        hashedPassword = passwordHandler.encryptPassword(str(password))
        databaseAccessor.insertUsernamePassword(username, hashedPassword)
        return self.SUCCESS

    def handleEmptyFields(self, username, password):
        isUsernameEmpty = self.checkTextEmpty(username)
        isPasswordEmpty = self.checkTextEmpty(password)

        if(isUsernameEmpty and isPasswordEmpty):
            return self.ERROR_EMPTY_FIELDS
        elif(isUsernameEmpty):
            return self.ERROR_EMPTY_USERNAME
        elif(isPasswordEmpty):
            return self.ERROR_EMPTY_PASSWORD
        else:
            return self.SUCCESS_FIELDS_FILLED

    def checkInputLength(self, inputType, input):
        if(inputType == 'USERNAME'):
            # username must be within 6-35 chars
            return len(input) >= 6 and len(input) <= 35
        elif(inputType == 'PASSWORD'):
            # password must be within 8-65 chars
            return len(input) >= 8 and len(input) <= 65

    def checkTextEmpty(self, text):
        if(text == ''):
            return True
        else:
            return False
