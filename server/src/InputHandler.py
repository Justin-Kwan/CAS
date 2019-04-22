from InputSanitizer import InputSanitizer
from PasswordEncryptor import PasswordEncryptor
from DatabaseAccessor import DatabaseAccessor

inputSanitizer = InputSanitizer()
passwordEncryptor = PasswordEncryptor()
databaseAccessor = DatabaseAccessor()

class InputHandler():

    ERROR_DUPLICATE_USERNAME = 'DUPLICATE_USERNAME'
    ERROR_EMPTY_FIELDS       = 'EMPTY_FIELDS'
    ERROR_EMPTY_USERNAME     = 'EMPTY_USERNAME'
    ERROR_EMPTY_PASSWORD     = 'EMPTY_PASSWORD'
    SUCCESS_FIELDS_FILLED    = 'ALL_FIELDS_FILLED'
    SUCCESS                  = 'SUCCESS'

    def handleUserInput(self, username, password):

        fieldEmptyCheckResult = self.handleEmptyFields(username, password)
        if(fieldEmptyCheckResult != self.SUCCESS_FIELDS_FILLED):
            return fieldEmptyCheckResult

        sanitizedUsername = inputSanitizer.sanitizeUsername(str(username))
        username = ''
        hashedPassword = passwordEncryptor.encryptPassword(str(password))
        password = ''

        doesUsernameExist = self.checkForExistingUsername(str(sanitizedUsername))
        if(doesUsernameExist):
            return self.ERROR_DUPLICATE_USERNAME

        databaseAccessor.insertUsernamePassword(sanitizedUsername, hashedPassword)
        sanitizedUsername = ''
        hashedPassword = ''

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

    def checkForExistingUsername(self, sanitizedUsername):
        selectedUsername = databaseAccessor.selectUsername(sanitizedUsername)
        parsedSelectedUsername = self.parseSelectedField(selectedUsername)

        if(parsedSelectedUsername == sanitizedUsername):
            return True
        else:
            return False

    def parseSelectedField(self, selectedField):
        selectedField = str(selectedField)

        for currentChar in selectedField:
            if(currentChar == '[' or currentChar == ']' or currentChar == '(' or currentChar == ')' or currentChar == ',' or currentChar == "'"):
                selectedField = selectedField.replace(currentChar, '')
        return selectedField

    def checkTextEmpty(self, text):
        if(text == ''):
            return True
        else:
            return False
