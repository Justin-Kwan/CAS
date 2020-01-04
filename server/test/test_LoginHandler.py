import pytest
import sys
import os

THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
sys.path.append(THIS_FOLDER + '/../src/database-layer')
sys.path.append(THIS_FOLDER + '/../src/domain-layer/handlers')

from SignUpHandler    import SignUpHandler
from LoginHandler     import LoginHandler
from DatabaseAccessor import DatabaseAccessor
import jwt

signUpHandler = SignUpHandler()
loginHandler = LoginHandler()
DBA = DatabaseAccessor()

def test_handleUserLogin():
    DBA.createConnection()
    DBA.clearDatabase()

    # success test login
    signUpHandler.handleUserSignUp('fake@aol.ca', 'password123')
    response = loginHandler.handleUserLogin('fake@aol.ca', 'password123')
    assert response != None
    assert response['response code'] == 202
    userData = jwt.decode(response['response string'], 'fake_secret_key', algorithms=['HS256'])
    assert 'email' in userData
    assert 'fake@aol.ca' in userData.values()
    assert 'user id' in userData

    # success test login
    signUpHandler.handleUserSignUp('a@aol.ca', 'password345')
    response = loginHandler.handleUserLogin('a@aol.ca', 'password345')
    assert response != None
    assert response['response code'] == 202
    userData = jwt.decode(response['response string'], 'fake_secret_key', algorithms=['HS256'])
    assert 'email' in userData
    assert 'a@aol.ca' in userData.values()
    assert 'user id' in userData

    # fail test login with wrong password
    signUpHandler.handleUserSignUp('fake@aol.com', 'password567')
    response = loginHandler.handleUserLogin('fake@aol.com', 'password000')
    assert response['response string'] == "email or password wrong"
    assert response['response code'] == 401

    # fail test login with non-existent email
    signUpHandler.handleUserSignUp('real@aol.com', 'password789')
    response = loginHandler.handleUserLogin('faker@aol.com', 'password789')
    assert response['response string'] == "email or password wrong"
    assert response['response code'] == 401

    # fail test login with empty email & password strings
    response = loginHandler.handleUserLogin('', '')
    assert response['response string'] == 'email empty'
    assert response['response code'] == 400

    response = loginHandler.handleUserLogin('fakename4', '')
    assert response['response string'] == 'password empty'
    assert response['response code'] == 400

    response = loginHandler.handleUserLogin('', 'password345')
    assert response['response string'] == 'email empty'
    assert response['response code'] == 400

    # fail test login with null email & password
    response = loginHandler.handleUserLogin(None, None)
    assert response['response string'] == 'email null'
    assert response['response code'] == 400

    response = loginHandler.handleUserLogin('fakename4', None)
    assert response['response string'] == 'password null'
    assert response['response code'] == 400

    response = loginHandler.handleUserLogin(None, 'password345')
    assert response['response string'] == 'email null'
    assert response['response code'] == 400

    DBA.clearDatabase()
    DBA.closeConnection()
