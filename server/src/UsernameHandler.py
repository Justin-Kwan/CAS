from DatabaseAccessor import DatabaseAccessor

databaseAccessor = DatabaseAccessor()

class UsernameHandler():

    def checkForInvalidUsernameChars(self, username):
        for currentChar in username:
            if(currentChar.isalpha() == False and currentChar.isdigit() == False):
                return False
        return True

    def checkForExistingUsername(self, username):
        selectedUsername = databaseAccessor.selectUsername(username)
        parsedSelectedUsername = self.parseSelectedField(selectedUsername)

        if(parsedSelectedUsername == username):
            return True
        else:
            return False

    def parseSelectedField(self, selectedField):
        selectedField = str(selectedField)

        for currentChar in selectedField:
            if(currentChar == '[' or currentChar == ']' or currentChar == '(' or currentChar == ')' or currentChar == ',' or currentChar == "'"):
                selectedField = selectedField.replace(currentChar, '')
        return selectedField
