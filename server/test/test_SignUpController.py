import pytest
import sys
sys.path.append('/Users/justinkwan/Documents/WebApps/UserAuth/server/src/controllers')
from SignUpController import SignUpController
from DatabaseAccessor import DatabaseAccessor

signUpController = SignUpController()
databaseAccessor = DatabaseAccessor()

def test_handleUserSignUp():
    # empty field(s) tests
    assert signUpController.handleUserSignUp('', '') == 'EMPTY_FIELDS'
    assert signUpController.handleUserSignUp('', 'password') == 'EMPTY_USERNAME'
    assert signUpController.handleUserSignUp('username', '') == 'EMPTY_PASSWORD'

    # success tests
    assert signUpController.handleUserSignUp('username1', 'password') == 'SUCCESS'
    assert signUpController.handleUserSignUp('username2', '        ') == 'SUCCESS'
    assert signUpController.handleUserSignUp('username3', '    )(*)    ') == 'SUCCESS'

    databaseAccessor.clearDatabase()

    # invalid username characters tests
    assert signUpController.handleUserSignUp('usern>ame', 'password') == 'INVALID_USERNAME_CHARS'
    assert signUpController.handleUserSignUp('-username', 'password') == 'INVALID_USERNAME_CHARS'
    assert signUpController.handleUserSignUp('username;', 'password') == 'INVALID_USERNAME_CHARS'
    assert signUpController.handleUserSignUp('{}{}{}{}{}', 'password') == 'INVALID_USERNAME_CHARS'

    # duplicate username tests
    databaseAccessor.insertUserInfo('username', 'password1', 'testId')
    assert signUpController.handleUserSignUp('username', 'password1') == 'DUPLICATE_USERNAME'
    databaseAccessor.clearDatabase()
    signUpController.handleUserSignUp('Username', 'password')
    assert signUpController.handleUserSignUp('username', 'password') == 'DUPLICATE_USERNAME'
    databaseAccessor.clearDatabase()
    signUpController.handleUserSignUp('username', 'password')
    assert signUpController.handleUserSignUp('Username', 'password') == 'DUPLICATE_USERNAME'
    databaseAccessor.clearDatabase()
    signUpController.handleUserSignUp('UsErNAME', 'password')
    assert signUpController.handleUserSignUp('USERNAME', 'password') == 'DUPLICATE_USERNAME'
    databaseAccessor.clearDatabase()
    signUpController.handleUserSignUp('USERNAME', 'password')
    assert signUpController.handleUserSignUp('username', 'password') == 'DUPLICATE_USERNAME'

    databaseAccessor.clearDatabase()

    # characters out of range in username or password tests
    assert signUpController.handleUserSignUp('testusernametestusernametestusername', 'testusernametestusernametestusernametestusernametestusernametestu;') == 'INVALID_USERNAME_LENGTH'
    assert signUpController.handleUserSignUp(',', 'testusernametestusernametestusernametestusernametestusernametestusername') == 'INVALID_USERNAME_LENGTH'
    assert signUpController.handleUserSignUp('User', '   ') == 'INVALID_USERNAME_LENGTH'
    assert signUpController.handleUserSignUp('Username1', 'testusernametestusernametestusernametestusernametestusernametestu;') == 'INVALID_PASSWORD_LENGTH'
    assert signUpController.handleUserSignUp('Username1', '*') == 'INVALID_PASSWORD_LENGTH'
    assert signUpController.handleUserSignUp('Username2', ' ') == 'INVALID_PASSWORD_LENGTH'
    assert signUpController.handleUserSignUp('GoodUsername', 'GoodPassword123') == 'SUCCESS'

    databaseAccessor.clearDatabase()

def test_getUser():
    user = signUpController.getUser('username1', 'password1')
    assert user.getUsername() == 'username1'
    assert user.getTextPassword() == 'password1'
    assert user.getHashedPassword() != None
    assert user.getUserId() != None
    assert len(user.getUserId()) == 36

    del user
