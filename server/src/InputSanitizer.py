
class InputSanitizer():

    sanitizedUsername = ''

    def sanitizeUsername(self, username):

        self.sanitizedUsername = ''

        for currentChar in username:
            if(currentChar.isalpha() == False and currentChar.isdigit() == False):
                username = username.replace(currentChar, '')

        self.sanitizedUsername = username
        username = ''

        return str(self.sanitizedUsername)
