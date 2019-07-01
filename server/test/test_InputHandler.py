import pytest
import sys
sys.path.append('/Users/justinkwan/Documents/WebApps/UserAuth/server/src')
from InputHandler     import InputHandler
from DatabaseAccessor import DatabaseAccessor

inputHandler     = InputHandler()
databaseAccessor = DatabaseAccessor()

def test_checkTextEmpty():
    assert inputHandler.checkTextEmpty('Not Empty') == False
    assert inputHandler.checkTextEmpty('') == True
    assert inputHandler.checkTextEmpty('0987*') == False

# testing username and password length constraints for input validation
def test_checkInputLength():
    # middle case
    assert inputHandler.checkInputLength('USERNAME', 'testusername') == True
    # edge case
    assert inputHandler.checkInputLength('USERNAME', 'usrnmm') == True
    assert inputHandler.checkInputLength('USERNAME', 'testusernametestusernametestusernam') == True
    assert inputHandler.checkInputLength('USERNAME', 'testusernametestusernametestusername') == False
    assert inputHandler.checkInputLength('USERNAME', 'usrnm') == False
    assert inputHandler.checkInputLength('USERNAME', '') == False
    assert inputHandler.checkInputLength('USERNAME', 'testusernametestusernametestusernametestusernametestusernametestusername') == False

    assert inputHandler.checkInputLength('PASSWORD', 'usrnmmff') == True
    assert inputHandler.checkInputLength('PASSWORD', 'testusernametestusernametestusernam') == True
    assert inputHandler.checkInputLength('PASSWORD', 'testusernametestusernametestusernametestusernametestusernametestu;') == False
    assert inputHandler.checkInputLength('PASSWORD', 'usrnmdd') == False
    assert inputHandler.checkInputLength('PASSWORD', '') == False
    assert inputHandler.checkInputLength('PASSWORD', 'testusernametestusernametestusernametestusernametestusernametestu') == True
    assert inputHandler.checkInputLength('PASSWORD', 'testusernametestusernametestusernametestusernametestusernametestusername') == False

def test_handleEmptyFields():
    assert inputHandler.handleEmptyFields('', '') == 'EMPTY_FIELDS'
    assert inputHandler.handleEmptyFields('', 'password') == 'EMPTY_USERNAME'
    assert inputHandler.handleEmptyFields('username', '') == 'EMPTY_PASSWORD'
    assert inputHandler.handleEmptyFields('username', 'password') == 'ALL_FIELDS_FILLED'

def test_handleInputLengthChecks():
    assert inputHandler.handleInputLengthChecks('NewUser123', 'testusername') == 'GOOD_USERNAME_&_PASSWORD_LENGTH'
    assert inputHandler.handleInputLengthChecks('usrnmm', 'testusernametestusernametestusernam') == 'GOOD_USERNAME_&_PASSWORD_LENGTH'
    assert inputHandler.handleInputLengthChecks('testusernametestusernametestusername', 'testusernametestusernametestusernametestusernametestusernametestu;') == 'INVALID_USERNAME_LENGTH'
    assert inputHandler.handleInputLengthChecks('', 'usrnmdd') == 'INVALID_USERNAME_LENGTH'
    assert inputHandler.handleInputLengthChecks('User', '') == 'INVALID_USERNAME_LENGTH'
    assert inputHandler.handleInputLengthChecks(',', 'testusernametestusernametestusernametestusernametestusernametestusername') == 'INVALID_USERNAME_LENGTH'
    assert inputHandler.handleInputLengthChecks('usrnmm', 'testusernametestusernametestusernametestusernametestusernametestu') == 'GOOD_USERNAME_&_PASSWORD_LENGTH'
    assert inputHandler.handleInputLengthChecks('usrnmm', 'testusernametestusernametestusernametestusernametestusernametestus') == 'INVALID_PASSWORD_LENGTH'
    assert inputHandler.handleInputLengthChecks('usrnmm', 'passwor') == 'INVALID_PASSWORD_LENGTH'

def test_checkForInvalidUsernameChars():
    assert inputHandler.checkForInvalidUsernameChars("string2") == True
    assert inputHandler.checkForInvalidUsernameChars("fake$username)") == False
    assert inputHandler.checkForInvalidUsernameChars(")(*&^)") == False
    assert inputHandler.checkForInvalidUsernameChars(")(*&^)textTest*&^%moretestis*fun';:") == False

def test_parseSelectedField():
    assert inputHandler.parseSelectedField('hello') == 'hello'
    assert inputHandler.parseSelectedField("[(',hello')]") == 'hello'
    assert inputHandler.parseSelectedField('[(,)') == ''

def test_checkForExistingUsername():
    databaseAccessor.clearDatabase()

    databaseAccessor.insertUserInfo('randomename1', 'teddddstPassword1', 'testId')
    databaseAccessor.insertUserInfo('anotherrand0mName', 'testPawddassword2', 'testId')
    databaseAccessor.insertUserInfo('09876543', 'test', 'testId')
    databaseAccessor.insertUserInfo('johnnotrealperson', 'password123', 'testId')
    doesUsernameExist = inputHandler.checkForExistingUsername('09876543')
    assert doesUsernameExist == True

    databaseAccessor.clearDatabase()

    databaseAccessor.insertUserInfo('robertH', 'teddddstPassword1', 'testId')
    databaseAccessor.insertUserInfo('william', 'testPawddassword2', 'testId')
    databaseAccessor.insertUserInfo('Johnathan', 'test', 'testId')
    databaseAccessor.insertUserInfo('randomguy', 'password123', 'testId')
    doesUsernameExist = inputHandler.checkForExistingUsername('johnathan')
    assert doesUsernameExist == False

    databaseAccessor.clearDatabase()

    databaseAccessor.insertUserInfo('001', 'teddddstPassword1', 'testId')
    databaseAccessor.insertUserInfo('02000000009', 'testPawddassword2', 'testId')
    databaseAccessor.insertUserInfo('joe', 'test', 'testId')
    databaseAccessor.insertUserInfo('testname', 'password123', 'testId')
    doesUsernameExist = inputHandler.checkForExistingUsername('02000000009')
    assert doesUsernameExist == True

    databaseAccessor.clearDatabase()
