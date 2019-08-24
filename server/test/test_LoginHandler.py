import pytest
import sys
sys.path.append('/Users/justinkwan/Documents/WebApps/UserAuth/server/src/BusinessLayer/handlers')
sys.path.append('/Users/justinkwan/Documents/WebApps/UserAuth/server/src/DataBaseLayer')
from SignUpHandler    import SignUpHandler
from LoginHandler     import LoginHandler
from DatabaseAccessor import DatabaseAccessor
import jwt

signUpHandler = SignUpHandler()
loginHandler = LoginHandler()
DBA = DatabaseAccessor()

RESULT_CODE = 1
AUTH_TOKEN  = 0


def test_handleUserLogin():
    DBA.createConnection()
    DBA.clearDatabase()

    # success test login
    signUpHandler.handleUserSignUp('fakename1', 'password123')
    resultPackage = loginHandler.handleUserLogin('fakename1', 'password123')
    assert resultPackage != None
    userData = jwt.decode(resultPackage[AUTH_TOKEN], 'fake_secret_key', algorithms=['HS256'])
    assert 'username' in userData
    assert 'fakename1' in userData.values()
    assert 'user id' in userData

    # success test login
    signUpHandler.handleUserSignUp('fakename2', 'password345')
    resultPackage = loginHandler.handleUserLogin('fakename2', 'password345')
    assert resultPackage != None
    userData = jwt.decode(resultPackage[AUTH_TOKEN], 'fake_secret_key', algorithms=['HS256'])
    assert 'username' in userData
    assert 'fakename2' in userData.values()
    assert 'user id' in userData

    # fail test login with wrong password
    signUpHandler.handleUserSignUp('fakename3', 'password567')
    resultPackage = loginHandler.handleUserLogin('fakename3', 'password000')
    assert resultPackage[RESULT_CODE] == 'INVALID_USERNAME_OR_PASSWORD'
    assert resultPackage[AUTH_TOKEN] == 'NO_TOKEN'

    # fail test login with non-existent username
    signUpHandler.handleUserSignUp('fakename4', 'password789')
    resultPackage = loginHandler.handleUserLogin('fakename0', 'password789')
    assert resultPackage[RESULT_CODE] == 'INVALID_USERNAME_OR_PASSWORD'
    assert resultPackage[AUTH_TOKEN] == 'NO_TOKEN'

    # fail test login with empty username & password strings
    resultPackage = loginHandler.handleUserLogin('', '')
    assert resultPackage[RESULT_CODE] == 'EMPTY_FIELDS'
    assert resultPackage[AUTH_TOKEN] == 'NO_TOKEN'
    resultPackage = loginHandler.handleUserLogin('fakename4', '')
    assert resultPackage[RESULT_CODE] == 'EMPTY_PASSWORD'
    assert resultPackage[AUTH_TOKEN] == 'NO_TOKEN'
    resultPackage = loginHandler.handleUserLogin('', 'password345')
    assert resultPackage[RESULT_CODE] == 'EMPTY_USERNAME'
    assert resultPackage[AUTH_TOKEN] == 'NO_TOKEN'

    # fail test login with null username & password
    resultPackage = loginHandler.handleUserLogin(None, None)
    assert resultPackage[RESULT_CODE] == 'EMPTY_FIELDS'
    assert resultPackage[AUTH_TOKEN] == 'NO_TOKEN'
    resultPackage = loginHandler.handleUserLogin('fakename4', None)
    assert resultPackage[RESULT_CODE] == 'EMPTY_PASSWORD'
    assert resultPackage[AUTH_TOKEN] == 'NO_TOKEN'
    resultPackage = loginHandler.handleUserLogin(None, 'password345')
    assert resultPackage[RESULT_CODE] == 'EMPTY_USERNAME'
    assert resultPackage[AUTH_TOKEN] == 'NO_TOKEN'

    DBA.clearDatabase()
    DBA.closeConnection()

def test_getUser():
    DBA.createConnection()
    user = loginHandler.getUser('username1', 'password1')
    assert user.getUsername() == 'username1'
    assert user.getTextPassword() == 'password1'
    assert user.getHashedPassword() == None
    assert user.getUserId() == None

    del user
    DBA.clearDatabase()
    DBA.closeConnection()
