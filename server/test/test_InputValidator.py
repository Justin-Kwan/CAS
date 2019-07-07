import pytest
import sys
sys.path.append('/Users/justinkwan/Documents/WebApps/UserAuth/server/src/BusinessLayer/handlers')
sys.path.append('/Users/justinkwan/Documents/WebApps/UserAuth/server/src/BusinessLayer/models')
sys.path.append('/Users/justinkwan/Documents/WebApps/UserAuth/server/src/BusinessLayer')
sys.path.append('/Users/justinkwan/Documents/WebApps/UserAuth/server/src/DataBaseLayer')
from InputValidator   import InputValidator
from DatabaseAccessor import DatabaseAccessor
from User             import User

inputValidator = InputValidator()
DBA = DatabaseAccessor()

def getUser(username, password):
    user = User(username, password)
    user.encryptAndUpdatePassword(password)
    user.generateAndUpdateUserId()
    return user

def test_checkInputNull():
    assert inputValidator.checkInputNull(None, None) == 'EMPTY_FIELDS'
    assert inputValidator.checkInputNull(None, 'password123') == 'EMPTY_USERNAME'
    assert inputValidator.checkInputNull('username123', None) == 'EMPTY_PASSWORD'
    assert inputValidator.checkInputNull('username123', 'password123') == 'ALL_FIELDS_FILLED'

def test_checkInputEmpty():
    assert inputValidator.checkInputEmpty('Not Empty') == False
    assert inputValidator.checkInputEmpty('') == True
    assert inputValidator.checkInputEmpty('0987*') == False

# testing username and password length constraints for input validation
def test_verifyInputLength():
    # middle case
    assert inputValidator.verifyInputLength('USERNAME', 'testusername') == True
    # edge case
    assert inputValidator.verifyInputLength('USERNAME', 'usrnmm') == True
    assert inputValidator.verifyInputLength('USERNAME', 'testusernametestusernametestusernam') == True
    assert inputValidator.verifyInputLength('USERNAME', 'testusernametestusernametestusername') == False
    assert inputValidator.verifyInputLength('USERNAME', 'usrnm') == False
    assert inputValidator.verifyInputLength('USERNAME', '') == False
    assert inputValidator.verifyInputLength('USERNAME', 'testusernametestusernametestusernametestusernametestusernametestusername') == False

    assert inputValidator.verifyInputLength('PASSWORD', 'usrnmmff') == True
    assert inputValidator.verifyInputLength('PASSWORD', 'testusernametestusernametestusernam') == True
    assert inputValidator.verifyInputLength('PASSWORD', 'testusernametestusernametestusernametestusernametestusernametestu;') == False
    assert inputValidator.verifyInputLength('PASSWORD', 'usrnmdd') == False
    assert inputValidator.verifyInputLength('PASSWORD', '') == False
    assert inputValidator.verifyInputLength('PASSWORD', 'testusernametestusernametestusernametestusernametestusernametestu') == True
    assert inputValidator.verifyInputLength('PASSWORD', 'testusernametestusernametestusernametestusernametestusernametestusername') == False

def test_handleEmptyInputFields():
    user = getUser('', '')
    assert inputValidator.handleEmptyInputFields(user) == 'EMPTY_FIELDS'
    del user

    user = getUser('', 'password')
    assert inputValidator.handleEmptyInputFields(user) == 'EMPTY_USERNAME'
    del user

    user = getUser('username', '')
    assert inputValidator.handleEmptyInputFields(user) == 'EMPTY_PASSWORD'
    del user

    user = getUser('username', 'password')
    assert inputValidator.handleEmptyInputFields(user) == 'ALL_FIELDS_FILLED'
    del user

def test_handleInputLengthChecks():
    user = getUser('NewUser123', 'testusername')
    assert inputValidator.handleInputLengthChecks(user) == 'GOOD_USERNAME_&_PASSWORD_LENGTH'
    del user

    user = getUser('usrnmm', 'testusernametestusernametestusernam')
    assert inputValidator.handleInputLengthChecks(user) == 'GOOD_USERNAME_&_PASSWORD_LENGTH'
    del user

    user = getUser('testusernametestusernametestusername', 'testusernametestusernametestusernametestusernametestusernametestu;')
    assert inputValidator.handleInputLengthChecks(user) == 'INVALID_USERNAME_LENGTH'
    del user

    user = getUser('', 'usrnmdd')
    assert inputValidator.handleInputLengthChecks(user) == 'INVALID_USERNAME_LENGTH'
    del user

    user = getUser('User', '')
    assert inputValidator.handleInputLengthChecks(user) == 'INVALID_USERNAME_LENGTH'
    del user

    user = getUser(',', 'testusernametestusernametestusernametestusernametestusernametestusername')
    assert inputValidator.handleInputLengthChecks(user) == 'INVALID_USERNAME_LENGTH'
    del user

    user = getUser('usrnmm', 'testusernametestusernametestusernametestusernametestusernametestu')
    assert inputValidator.handleInputLengthChecks(user) == 'GOOD_USERNAME_&_PASSWORD_LENGTH'
    del user

    user = getUser('usrnmm', 'testusernametestusernametestusernametestusernametestusernametestus')
    assert inputValidator.handleInputLengthChecks(user) == 'INVALID_PASSWORD_LENGTH'
    del user

    user = getUser('usrnmm', 'passwor')
    assert inputValidator.handleInputLengthChecks(user) == 'INVALID_PASSWORD_LENGTH'
    del user

def test_verifyUsernameChars():
    user = getUser('string2', 'password123')
    assert inputValidator.verifyUsernameChars(user) == True
    del user

    user = getUser('fake$username)', 'password123')
    assert inputValidator.verifyUsernameChars(user) == False
    del user

    user = getUser(')(*&^)', 'password123')
    assert inputValidator.verifyUsernameChars(user) == False
    del user

    user = getUser(')(*&^)textTest*&^%moretestis*fun;:', 'password123')
    assert inputValidator.verifyUsernameChars(user) == False
    del user

def test_verifyPassword():
    user1 = getUser('username1', 'password1')
    DBA.insertUserInfo(user1)
    user2 = getUser('username1', 'password1')
    selectedHashedPassword = DBA.selectHashedPassword(user2).encode('utf-8')
    isPasswordCorrect = inputValidator.verifyPassword(user2, selectedHashedPassword)
    assert isPasswordCorrect == True

    del user1
    del user2
    DBA.clearDatabase()

    user1 = getUser('username2', 'password2')
    DBA.insertUserInfo(user1)
    user2 = getUser('username2', 'password1')
    selectedHashedPassword = DBA.selectHashedPassword(user2).encode('utf-8')
    isPasswordCorrect = inputValidator.verifyPassword(user2, selectedHashedPassword)
    assert isPasswordCorrect == False

    del user1
    del user2
    DBA.clearDatabase()

    user1 = getUser('username3', '^&*()()')
    DBA.insertUserInfo(user1)
    user2 = getUser('username3', '^&*()()')
    selectedHashedPassword = DBA.selectHashedPassword(user2).encode('utf-8')
    isPasswordCorrect = inputValidator.verifyPassword(user2, selectedHashedPassword)
    assert isPasswordCorrect == True

    del user1
    del user2
    DBA.clearDatabase()
