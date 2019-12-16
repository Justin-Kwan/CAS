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

RESPONSE_STRING = 0
RESPONSE_CODE   = 1

def test_handleUserLogin():
    DBA.createConnection()
    DBA.clearDatabase()

    # success test login
    signUpHandler.handleUserSignUp('fake@aol.ca', 'password123')
    resultPackage = loginHandler.handleUserLogin('fake@aol.ca', 'password123')
    assert resultPackage != None
    assert resultPackage[RESPONSE_CODE] == 202
    userData = jwt.decode(resultPackage[RESPONSE_STRING], 'fake_secret_key', algorithms=['HS256'])
    assert 'email' in userData
    assert 'fake@aol.ca' in userData.values()
    assert 'user id' in userData

    # success test login
    signUpHandler.handleUserSignUp('a@aol.c', 'password345')
    resultPackage = loginHandler.handleUserLogin('a@aol.c', 'password345')
    assert resultPackage != None
    assert resultPackage[RESPONSE_CODE] == 202
    userData = jwt.decode(resultPackage[RESPONSE_STRING], 'fake_secret_key', algorithms=['HS256'])
    assert 'email' in userData
    assert 'a@aol.c' in userData.values()
    assert 'user id' in userData

    # fail test login with wrong password
    signUpHandler.handleUserSignUp('fake@aol.com', 'password567')
    resultPackage = loginHandler.handleUserLogin('fake@aol.com', 'password000')
    assert resultPackage[RESPONSE_STRING] == "email or password wrong"
    assert resultPackage[RESPONSE_CODE] == 401

    # fail test login with non-existent email
    signUpHandler.handleUserSignUp('real@aol.com', 'password789')
    resultPackage = loginHandler.handleUserLogin('faker@aol.com', 'password789')
    assert resultPackage[RESPONSE_STRING] == "email or password wrong"
    assert resultPackage[RESPONSE_CODE] == 401

    # fail test login with empty email & password strings
    resultPackage = loginHandler.handleUserLogin('', '')
    assert resultPackage[RESPONSE_STRING] == 'email empty'
    assert resultPackage[RESPONSE_CODE] == 400


    resultPackage = loginHandler.handleUserLogin('fakename4', '')
    assert resultPackage[RESPONSE_STRING] == 'password empty'
    assert resultPackage[RESPONSE_CODE] == 400

    resultPackage = loginHandler.handleUserLogin('', 'password345')
    assert resultPackage[RESPONSE_STRING] == 'email empty'
    assert resultPackage[RESPONSE_CODE] == 400

    # fail test login with null email & password
    resultPackage = loginHandler.handleUserLogin(None, None)
    assert resultPackage[RESPONSE_STRING] == 'email null'
    assert resultPackage[RESPONSE_CODE] == 400

    resultPackage = loginHandler.handleUserLogin('fakename4', None)
    assert resultPackage[RESPONSE_STRING] == 'password null'
    assert resultPackage[RESPONSE_CODE] == 400

    resultPackage = loginHandler.handleUserLogin(None, 'password345')
    assert resultPackage[RESPONSE_STRING] == 'email null'
    assert resultPackage[RESPONSE_CODE] == 400

    DBA.clearDatabase()
    DBA.closeConnection()
