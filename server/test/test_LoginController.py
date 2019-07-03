import pytest
import sys
sys.path.append('/Users/justinkwan/Documents/WebApps/UserAuth/server/src/controllers')
from SignUpController import SignUpController
from LoginController import LoginController
from DatabaseAccessor import DatabaseAccessor
import jwt

signUpController = SignUpController()
loginController = LoginController()
DBA = DatabaseAccessor()

def test_handleUserLogin():
    DBA.clearDatabase()

    # success test login
    signUpController.handleUserSignUp('fakename1', 'password123')
    processResult = loginController.handleUserLogin('fakename1', 'password123')
    assert processResult != None
    userData = jwt.decode(processResult, 'fake_secret_key', algorithms=['HS256'])
    assert 'username' in userData
    assert 'fakename1' in userData.values()
    assert 'user id' in userData

    # success test login
    signUpController.handleUserSignUp('fakename2', 'password345')
    processResult = loginController.handleUserLogin('fakename2', 'password345')
    assert processResult != None
    userData = jwt.decode(processResult, 'fake_secret_key', algorithms=['HS256'])
    assert 'username' in userData
    assert 'fakename2' in userData.values()
    assert 'user id' in userData

    # fail test login with wrong password
    signUpController.handleUserSignUp('fakename3', 'password567')
    processResult = loginController.handleUserLogin('fakename3', 'password000')
    assert processResult == 'INVALID_USERNAME_OR_PASSWORD'

    # fail test login with non-existent username
    signUpController.handleUserSignUp('fakename4', 'password789')
    processResult = loginController.handleUserLogin('fakename0', 'password789')
    assert processResult == 'INVALID_USERNAME_OR_PASSWORD'

    # fail test login with empty username & password strings
    processResult = loginController.handleUserLogin('', '')
    assert processResult == 'EMPTY_FIELDS'
    processResult = loginController.handleUserLogin('fakename4', '')
    assert processResult == 'EMPTY_PASSWORD'
    processResult = loginController.handleUserLogin('', 'password345')
    assert processResult == 'EMPTY_USERNAME'

    # fail test login with null username & password
    processResult = loginController.handleUserLogin(None, None)
    assert processResult == 'EMPTY_FIELDS'
    processResult = loginController.handleUserLogin('fakename4', None)
    assert processResult == 'EMPTY_PASSWORD'
    processResult = loginController.handleUserLogin(None, 'password345')
    assert processResult == 'EMPTY_USERNAME'

    DBA.clearDatabase()

def test_getUser():
    user = loginController.getUser('username1', 'password1')
    assert user.getUsername() == 'username1'
    assert user.getTextPassword() == 'password1'
    assert user.getHashedPassword() == None
    assert user.getUserId() == None

    del user
    DBA.clearDatabase()
