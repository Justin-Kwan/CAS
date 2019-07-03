import pytest
import sys
sys.path.append('/Users/justinkwan/Documents/WebApps/UserAuth/server/src/controllers')
from SignUpController import SignUpController
from DatabaseAccessor import DatabaseAccessor

signUpController = SignUpController()
DBA = DatabaseAccessor()

def getUser(username, password):
    user = User(username, password)
    user.encryptAndUpdatePassword(password)
    user.generateAndUpdateUserId()
    return user

def test_handleUserSignUp():
    DBA.clearDatabase()

    # empty field(s) tests
    assert signUpController.handleUserSignUp('', '') == 'EMPTY_FIELDS'
    assert signUpController.handleUserSignUp(None, None) == 'EMPTY_FIELDS'
    assert signUpController.handleUserSignUp('', 'password') == 'EMPTY_USERNAME'
    assert signUpController.handleUserSignUp(None, 'password') == 'EMPTY_USERNAME'
    assert signUpController.handleUserSignUp('username', '') == 'EMPTY_PASSWORD'
    assert signUpController.handleUserSignUp('username', None) == 'EMPTY_PASSWORD'

    # success tests
    assert signUpController.handleUserSignUp('username1', 'password') == 'SUCCESS'
    assert signUpController.handleUserSignUp('username2', '        ') == 'SUCCESS'
    assert signUpController.handleUserSignUp('username3', '    )(*)    ') == 'SUCCESS'

    DBA.clearDatabase()

    # invalid username characters tests
    assert signUpController.handleUserSignUp('usern>ame', 'password') == 'INVALID_USERNAME_CHARS'
    assert signUpController.handleUserSignUp('-username', 'password') == 'INVALID_USERNAME_CHARS'
    assert signUpController.handleUserSignUp('username;', 'password') == 'INVALID_USERNAME_CHARS'
    assert signUpController.handleUserSignUp('{}{}{}{}{}', 'password') == 'INVALID_USERNAME_CHARS'

    # duplicate username tests
    signUpController.handleUserSignUp('username', 'password1')
    assert signUpController.handleUserSignUp('username', 'password1') == 'DUPLICATE_USERNAME'
    DBA.clearDatabase()
    signUpController.handleUserSignUp('Username', 'password')
    assert signUpController.handleUserSignUp('username', 'password') == 'DUPLICATE_USERNAME'
    DBA.clearDatabase()
    signUpController.handleUserSignUp('username', 'password')
    assert signUpController.handleUserSignUp('Username', 'password') == 'DUPLICATE_USERNAME'
    DBA.clearDatabase()
    signUpController.handleUserSignUp('UsErNAME', 'password')
    assert signUpController.handleUserSignUp('USERNAME', 'password') == 'DUPLICATE_USERNAME'
    DBA.clearDatabase()
    signUpController.handleUserSignUp('USERNAME', 'password')
    assert signUpController.handleUserSignUp('username', 'password') == 'DUPLICATE_USERNAME'

    DBA.clearDatabase()

    # characters out of range in username or password tests
    assert signUpController.handleUserSignUp('testusernametestusernametestusername', 'testusernametestusernametestusernametestusernametestusernametestu;') == 'INVALID_USERNAME_LENGTH'
    assert signUpController.handleUserSignUp(',', 'testusernametestusernametestusernametestusernametestusernametestusername') == 'INVALID_USERNAME_LENGTH'
    assert signUpController.handleUserSignUp('User', '   ') == 'INVALID_USERNAME_LENGTH'
    assert signUpController.handleUserSignUp('Username1', 'testusernametestusernametestusernametestusernametestusernametestu;') == 'INVALID_PASSWORD_LENGTH'
    assert signUpController.handleUserSignUp('Username1', '*') == 'INVALID_PASSWORD_LENGTH'
    assert signUpController.handleUserSignUp('Username2', ' ') == 'INVALID_PASSWORD_LENGTH'
    assert signUpController.handleUserSignUp('GoodUsername', 'GoodPassword123') == 'SUCCESS'

    DBA.clearDatabase()

def test_getUser():
    user = signUpController.getUser('username1', 'password1')
    assert user.getUsername() == 'username1'
    assert user.getTextPassword() == 'password1'
    assert user.getHashedPassword() != None
    assert user.getUserId() != None
    assert len(user.getUserId()) == 36

    del user
    DBA.clearDatabase()
