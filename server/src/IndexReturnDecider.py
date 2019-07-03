from ResultCodes import ResultCodes

resultCodes = ResultCodes()

class IndexReturnDecider():

    def determineSignUpRedirectPage(self, resultCode):
        if resultCode == resultCodes.SUCCESS:
            return 'signUpSuccess'
        elif resultCode == resultCodes.ERROR_DUPLICATE_USERNAME:
            return 'signUpExistingUsername'
        elif resultCode == resultCodes.ERROR_INVALID_USERNAME_CHARS:
            return 'signUpInvalidUsernameCharacters'
        elif resultCode == resultCodes.ERROR_USERNAME_LENGTH_INVALID:
            return 'signUpUsernameOutOfRange'
        elif resultCode == resultCodes.ERROR_PASSWORD_LENGTH_INVALID:
            return 'signUpPasswordOutOfRange'
        else:
            return 'signUpEmptyFields'

    def determineLoginRedirectPage(self, resultCode):
        if resultCode == resultCodes.ERROR_INVALID_USERNAME_OR_PASSWORD:
            return 'loginInvalidUsernameOrPassword'
        else:
            return 'loginEmptyFields'

    def checkIfTokenReturned(self, resultCode):
        if resultCode == resultCodes.SUCCESS:
            return True
        return False
