'''
    this class handles user input with functions pertaining to the username
    and password
'''

import bcrypt
from DatabaseAccessor import DatabaseAccessor
from ResultCodes      import ResultCodes

DBA = DatabaseAccessor()
resultCodes = ResultCodes()

class InputHandler():

    def checkInputNull(self, username, password):
        if(username == None and password == None):
            return resultCodes.ERROR_EMPTY_FIELDS
        elif(username == None and password != None):
            return resultCodes.ERROR_EMPTY_USERNAME
        elif(password == None and username != None):
            return resultCodes.ERROR_EMPTY_PASSWORD
        return resultCodes.SUCCESS_FIELDS_FILLED

    def handleEmptyFields(self, user):

        username = user.getUsername()
        password = user.getTextPassword()

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

    def checkTextEmpty(self, text):
        if(len(text) == 0):
            return True
        return False

    def handleInputLengthChecks(self, user):

        username = user.getUsername()
        password = user.getTextPassword()

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

    def checkInputLength(self, inputType, input):
        if(inputType == 'USERNAME'):
            return len(input) >= 6 and len(input) <= 35
        elif(inputType == 'PASSWORD'):
            return len(input) >= 8 and len(input) <= 65

    def checkForInvalidUsernameChars(self, user):
        username = user.getUsername()

        for currentChar in username:
            if(currentChar.isalpha() == False and currentChar.isdigit() == False):
                return False
        return True

    def checkForExistingUsername(self, user):
        selectedUsername = DBA.selectUsername(user)
        return selectedUsername == user.getUsername()
        
    def verifyPassword(self, user):
        password = user.getTextPassword().encode('utf-8')
        selectedHashedPassword = DBA.selectHashedPassword(user).encode('utf-8')

        if(bcrypt.checkpw(password, selectedHashedPassword) == False):
            return False
        return True
