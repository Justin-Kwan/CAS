import pytest
import sys
sys.path.append('/Users/justinkwan/Documents/WebApps/UserAuth/server/src/handlers')
from SignUpHandler import SignUpHandler
from DatabaseAccessor import DatabaseAccessor

signUpHandler = SignUpHandler()
DBA = DatabaseAccessor()

def getUser(username, password):
    user = User(username, password)
    user.encryptAndUpdatePassword(password)
    user.generateAndUpdateUserId()
    return user

def test_handleUserSignUp():
    DBA.clearDatabase()

    # empty field(s) tests
    assert signUpHandler.handleUserSignUp('', '') == 'EMPTY_FIELDS'
    assert signUpHandler.handleUserSignUp(None, None) == 'EMPTY_FIELDS'
    assert signUpHandler.handleUserSignUp('', 'password') == 'EMPTY_USERNAME'
    assert signUpHandler.handleUserSignUp(None, 'password') == 'EMPTY_USERNAME'
    assert signUpHandler.handleUserSignUp('username', '') == 'EMPTY_PASSWORD'
    assert signUpHandler.handleUserSignUp('username', None) == 'EMPTY_PASSWORD'

    # success tests
    assert signUpHandler.handleUserSignUp('username1', 'password') == 'SUCCESS'
    assert signUpHandler.handleUserSignUp('username2', '        ') == 'SUCCESS'
    assert signUpHandler.handleUserSignUp('username3', '    )(*)    ') == 'SUCCESS'

    DBA.clearDatabase()

    # invalid username characters tests
    assert signUpHandler.handleUserSignUp('usern>ame', 'password') == 'INVALID_USERNAME_CHARS'
    assert signUpHandler.handleUserSignUp('-username', 'password') == 'INVALID_USERNAME_CHARS'
    assert signUpHandler.handleUserSignUp('username;', 'password') == 'INVALID_USERNAME_CHARS'
    assert signUpHandler.handleUserSignUp('{}{}{}{}{}', 'password') == 'INVALID_USERNAME_CHARS'

    # duplicate username tests
    signUpHandler.handleUserSignUp('username', 'password1')
    assert signUpHandler.handleUserSignUp('username', 'password1') == 'DUPLICATE_USERNAME'
    DBA.clearDatabase()
    signUpHandler.handleUserSignUp('Username', 'password')
    assert signUpHandler.handleUserSignUp('username', 'password') == 'DUPLICATE_USERNAME'
    DBA.clearDatabase()
    signUpHandler.handleUserSignUp('username', 'password')
    assert signUpHandler.handleUserSignUp('Username', 'password') == 'DUPLICATE_USERNAME'
    DBA.clearDatabase()
    signUpHandler.handleUserSignUp('UsErNAME', 'password')
    assert signUpHandler.handleUserSignUp('USERNAME', 'password') == 'DUPLICATE_USERNAME'
    DBA.clearDatabase()
    signUpHandler.handleUserSignUp('USERNAME', 'password')
    assert signUpHandler.handleUserSignUp('username', 'password') == 'DUPLICATE_USERNAME'

    DBA.clearDatabase()

    # characters out of range in username or password tests
    assert signUpHandler.handleUserSignUp('testusernametestusernametestusername', 'testusernametestusernametestusernametestusernametestusernametestu;') == 'INVALID_USERNAME_LENGTH'
    assert signUpHandler.handleUserSignUp(',', 'testusernametestusernametestusernametestusernametestusernametestusername') == 'INVALID_USERNAME_LENGTH'
    assert signUpHandler.handleUserSignUp('User', '   ') == 'INVALID_USERNAME_LENGTH'
    assert signUpHandler.handleUserSignUp('Username1', 'testusernametestusernametestusernametestusernametestusernametestu;') == 'INVALID_PASSWORD_LENGTH'
    assert signUpHandler.handleUserSignUp('Username1', '*') == 'INVALID_PASSWORD_LENGTH'
    assert signUpHandler.handleUserSignUp('Username2', ' ') == 'INVALID_PASSWORD_LENGTH'
    assert signUpHandler.handleUserSignUp('GoodUsername', 'GoodPassword123') == 'SUCCESS'

    DBA.clearDatabase()

def test_getUser():
    user = signUpHandler.getUser('username1', 'password1')
    assert user.getUsername() == 'username1'
    assert user.getTextPassword() == 'password1'
    assert user.getHashedPassword() != None
    assert user.getUserId() != None
    assert len(user.getUserId()) == 36

    del user
    DBA.clearDatabase()
