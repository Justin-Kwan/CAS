'''
    this class handles user input with functions that pertain to the username
    and password
'''

import bcrypt
from DatabaseAccessor import DatabaseAccessor
from ResultCodes import ResultCodes

databaseAccessor = DatabaseAccessor()
resultCodes = ResultCodes()

class InputHandler():

    def handleEmptyFields(self, username, password):
        isUsernameEmpty = self.checkTextEmpty(username)
        isPasswordEmpty = self.checkTextEmpty(password)

        if(isUsernameEmpty and isPasswordEmpty):
            return resultCodes.ERROR_EMPTY_FIELDS
        elif(isUsernameEmpty):
            return resultCodes.ERROR_EMPTY_USERNAME
        elif(isPasswordEmpty):
            return resultCodes.ERROR_EMPTY_PASSWORD
        else:
            return resultCodes.SUCCESS_FIELDS_FILLED

    def handleInputLengthChecks(self, username, password):
        isUsernameLengthOk = self.checkInputLength('USERNAME', username)
        isPasswordLengthOk = self.checkInputLength('PASSWORD', password)

        if(isUsernameLengthOk == True and isPasswordLengthOk == True):
            return resultCodes.SUCCESS_USERNAME_PASSWORD_LENGTH
        elif(isUsernameLengthOk == False and isPasswordLengthOk == True):
            return resultCodes.ERROR_USERNAME_LENGTH_INVALID
        elif(isUsernameLengthOk == True and isPasswordLengthOk == False):
            return resultCodes.ERROR_PASSWORD_LENGTH_INVALID
        else:
            return resultCodes.ERROR_USERNAME_LENGTH_INVALID

    def checkTextEmpty(self, text):
        return text == ''

    def checkInputLength(self, inputType, input):
        if(inputType == 'USERNAME'):
            return len(input) >= 6 and len(input) <= 35
        elif(inputType == 'PASSWORD'):
            return len(input) >= 8 and len(input) <= 65

    def checkForInvalidUsernameChars(self, username):
        for currentChar in username:
            if(currentChar.isalpha() == False and currentChar.isdigit() == False):
                return False
        return True

    def checkForExistingUsername(self, username):
        selectedUsername = databaseAccessor.selectUsername(username)
        parsedSelectedUsername = self.parseSelectedField(selectedUsername)
        return parsedSelectedUsername == username

    def parseSelectedField(self, selectedField):
        selectedField = str(selectedField)

        for currentChar in selectedField:
            if(currentChar == '[' or currentChar == ']' or currentChar == '(' or currentChar == ')' or currentChar == ',' or currentChar == "'"):
                selectedField = selectedField.replace(currentChar, '')
        return selectedField

    def encryptPassword(self, password):
        hashedPassword = bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt())
        return str(hashedPassword)

    # bcrypt.check_password_hash(pw_hash, 'testpassword') # returns True
