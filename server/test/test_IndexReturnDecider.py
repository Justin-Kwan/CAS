import pytest
import sys
sys.path.append('/Users/justinkwan/Documents/WebApps/UserAuth/server/src/PresentationLayer')
sys.path.append('/Users/justinkwan/Documents/WebApps/UserAuth/server/src')
from IndexReturnDecider import IndexReturnDecider
from ResultCodes        import ResultCodes

IRD = IndexReturnDecider()
resultCodes = ResultCodes()

def test_determineSignUpRedirectPage():
    assert IRD.determineSignUpRedirectPage(resultCodes.SUCCESS) == 'signUpSuccess'
    assert IRD.determineSignUpRedirectPage(resultCodes.ERROR_DUPLICATE_USERNAME) == 'signUpExistingUsername'
    assert IRD.determineSignUpRedirectPage(resultCodes.ERROR_INVALID_USERNAME_CHARS) == 'signUpInvalidUsernameCharacters'
    assert IRD.determineSignUpRedirectPage(resultCodes.ERROR_USERNAME_LENGTH_INVALID) == 'signUpUsernameOutOfRange'
    assert IRD.determineSignUpRedirectPage(resultCodes.ERROR_PASSWORD_LENGTH_INVALID) == 'signUpPasswordOutOfRange'
    assert IRD.determineSignUpRedirectPage(resultCodes.ERROR_EMPTY_FIELDS) == 'signUpEmptyFields'
    assert IRD.determineSignUpRedirectPage(resultCodes.ERROR_EMPTY_PASSWORD) == 'signUpEmptyFields'
    assert IRD.determineSignUpRedirectPage(resultCodes.ERROR_EMPTY_USERNAME) == 'signUpEmptyFields'

def test_determineLoginRedirectPage():
    assert IRD.determineLoginRedirectPage(resultCodes.ERROR_INVALID_USERNAME_OR_PASSWORD) == 'loginInvalidUsernameOrPassword'
    assert IRD.determineLoginRedirectPage(resultCodes.ERROR_EMPTY_FIELDS) == 'loginEmptyFields'
    assert IRD.determineLoginRedirectPage(resultCodes.ERROR_EMPTY_USERNAME) == 'loginEmptyFields'
    assert IRD.determineLoginRedirectPage(resultCodes.ERROR_EMPTY_PASSWORD) == 'loginEmptyFields'

def test_checkIfTokenReturned():
    assert IRD.checkIfTokenReturned(resultCodes.SUCCESS) == True
    assert IRD.checkIfTokenReturned(resultCodes.ERROR_INVALID_USERNAME_OR_PASSWORD) == False
    assert IRD.checkIfTokenReturned(resultCodes.ERROR_EMPTY_FIELDS) == False
    assert IRD.checkIfTokenReturned(resultCodes.ERROR_EMPTY_USERNAME) == False
    assert IRD.checkIfTokenReturned(resultCodes.ERROR_EMPTY_PASSWORD) == False
