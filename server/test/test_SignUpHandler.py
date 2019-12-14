import pytest
import sys
sys.path.append('/Users/justinkwan/Documents/WebApps/UserAuth/server/src/BusinessLayer/handlers')
sys.path.append('/Users/justinkwan/Documents/WebApps/UserAuth/server/src/DataBaseLayer')
from SignUpHandler import SignUpHandler
from DatabaseAccessor import DatabaseAccessor

RESPONSE_STRING = 0
RESPONSE_CODE   = 1

signUpHandler = SignUpHandler()
DBA = DatabaseAccessor()

def getUser(username, password):
    user = User(username, password)
    user.encryptAndSetPassword(password)
    user.generateAndUpdateUserId()
    return user

def test_handleUserSignUp():
    DBA.createConnection()
    DBA.clearDatabase()

    # empty field(s) tests
    resultPackage = signUpHandler.handleUserSignUp('', '')
    assert resultPackage[RESPONSE_STRING] == 'username empty'
    assert resultPackage[RESPONSE_CODE] == 400

    resultPackage = signUpHandler.handleUserSignUp(None, None)
    assert resultPackage[RESPONSE_STRING] == 'username null'
    assert resultPackage[RESPONSE_CODE] == 400

    resultPackage = signUpHandler.handleUserSignUp('', 'password')
    assert resultPackage[RESPONSE_STRING] == 'username empty'
    assert resultPackage[RESPONSE_CODE] == 400

    resultPackage = signUpHandler.handleUserSignUp(None, 'password')
    assert resultPackage[RESPONSE_STRING] == 'username null'
    assert resultPackage[RESPONSE_CODE] == 400

    resultPackage = signUpHandler.handleUserSignUp('username', '')
    assert resultPackage[RESPONSE_STRING] == 'password empty'
    assert resultPackage[RESPONSE_CODE] == 400

    resultPackage = signUpHandler.handleUserSignUp('username', None)
    assert resultPackage[RESPONSE_STRING] == 'password null'
    assert resultPackage[RESPONSE_CODE] == 400

    # success tests
    resultPackage = signUpHandler.handleUserSignUp('username1', 'password')
    assert resultPackage[RESPONSE_STRING] == 'signup successful'
    assert resultPackage[RESPONSE_CODE] == 201

    resultPackage = signUpHandler.handleUserSignUp('username2', '        ')
    assert resultPackage[RESPONSE_STRING] == 'signup successful'
    assert resultPackage[RESPONSE_CODE] == 201

    resultPackage = signUpHandler.handleUserSignUp('username3', '    )(*)    ')
    assert resultPackage[RESPONSE_STRING] == 'signup successful'
    assert resultPackage[RESPONSE_CODE] == 201

    DBA.clearDatabase()

    # invalid username characters tests

    resultPackage = signUpHandler.handleUserSignUp('usern>ame', 'password')
    assert resultPackage[RESPONSE_STRING] == 'username characters bad'
    assert resultPackage[RESPONSE_CODE] == 400

    resultPackage = signUpHandler.handleUserSignUp('-username', 'password')
    assert resultPackage[RESPONSE_STRING] == 'username characters bad'
    assert resultPackage[RESPONSE_CODE] == 400

    resultPackage = signUpHandler.handleUserSignUp('username;', 'password')
    assert resultPackage[RESPONSE_STRING] == 'username characters bad'
    assert resultPackage[RESPONSE_CODE] == 400

    resultPackage = signUpHandler.handleUserSignUp('{}{}{}{}{}', 'password')
    assert resultPackage[RESPONSE_STRING] == 'username characters bad'
    assert resultPackage[RESPONSE_CODE] == 400

    # duplicate username tests
    signUpHandler.handleUserSignUp('username', 'password1')
    resultPackage = signUpHandler.handleUserSignUp('username', 'password1')
    assert resultPackage[RESPONSE_STRING] == 'username already exists'
    assert resultPackage[RESPONSE_CODE] == 400

    DBA.clearDatabase()

    signUpHandler.handleUserSignUp('Username', 'password')
    resultPackage = signUpHandler.handleUserSignUp('Username', 'password')
    assert resultPackage[RESPONSE_STRING] == 'username already exists'
    assert resultPackage[RESPONSE_CODE] == 400

    resultPackage = signUpHandler.handleUserSignUp('username', 'password')
    assert resultPackage[RESPONSE_STRING] == 'username already exists'
    assert resultPackage[RESPONSE_CODE] == 400

    DBA.clearDatabase()

    signUpHandler.handleUserSignUp('username', 'password')
    resultPackage = signUpHandler.handleUserSignUp('Username', 'password')
    assert resultPackage[RESPONSE_STRING] == 'username already exists'
    assert resultPackage[RESPONSE_CODE] == 400

    DBA.clearDatabase()

    signUpHandler.handleUserSignUp('UsErNAME', 'password')
    resultPackage = signUpHandler.handleUserSignUp('USERNAME', 'password')
    assert resultPackage[RESPONSE_STRING] == 'username already exists'
    assert resultPackage[RESPONSE_CODE] == 400

    DBA.clearDatabase()

    signUpHandler.handleUserSignUp('USERNAME', 'password')
    resultPackage = signUpHandler.handleUserSignUp('username', 'password')
    assert resultPackage[RESPONSE_STRING] == 'username already exists'
    assert resultPackage[RESPONSE_CODE] == 400

    DBA.clearDatabase()

    # characters out of range in username or password tests
    resultPackage = signUpHandler.handleUserSignUp('testusernametestusernametestusername', 'testusernametestusernametestusernametestusernametestusernametestu;')
    assert resultPackage[RESPONSE_STRING] == "username length bad"
    assert resultPackage[RESPONSE_CODE] == 400

    resultPackage = signUpHandler.handleUserSignUp(',', 'testusernametestusernametestusernametestusernametestusernametestusername')
    assert resultPackage[RESPONSE_STRING] == "username length bad"
    assert resultPackage[RESPONSE_CODE] == 400

    resultPackage = signUpHandler.handleUserSignUp('User', '   ')
    assert resultPackage[RESPONSE_STRING] == "username length bad"
    assert resultPackage[RESPONSE_CODE] == 400

    resultPackage = signUpHandler.handleUserSignUp('Username1', 'testusernametestusernametestusernametestusernametestusernametestu;')
    assert resultPackage[RESPONSE_STRING] == "password length bad"
    assert resultPackage[RESPONSE_CODE] == 400

    resultPackage = signUpHandler.handleUserSignUp('Username1', '*')
    assert resultPackage[RESPONSE_STRING] == "password length bad"
    assert resultPackage[RESPONSE_CODE] == 400

    resultPackage = signUpHandler.handleUserSignUp('Username2', ' ')
    assert resultPackage[RESPONSE_STRING] == "password length bad"
    assert resultPackage[RESPONSE_CODE] == 400

    resultPackage = signUpHandler.handleUserSignUp('GoodUsername', 'GoodPassword123')
    assert resultPackage[RESPONSE_STRING] == 'signup successful'
    assert resultPackage[RESPONSE_CODE] == 201

    DBA.clearDatabase()
    DBA.closeConnection()

def test_getUser():
    DBA.createConnection()
    user = signUpHandler.getUser('username1', 'password1')
    assert user.getUsername() == 'username1'
    assert user.getTextPassword() == 'password1'
    assert user.getHashedPassword() != None
    assert user.getUserId() != None
    assert len(user.getUserId()) == 36

    del user
    DBA.clearDatabase()
    DBA.closeConnection()
