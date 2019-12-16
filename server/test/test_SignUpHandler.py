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

def getUser(email, password):
    user = User(email, password)
    user.encryptAndSetPassword(password)
    user.generateAndUpdateUserId()
    return user

def test_handleUserSignUp():
    DBA.createConnection()
    DBA.clearDatabase()

    # empty field(s) tests
    resultPackage = signUpHandler.handleUserSignUp('', '')
    assert resultPackage[RESPONSE_STRING] == 'email empty'
    assert resultPackage[RESPONSE_CODE] == 400

    resultPackage = signUpHandler.handleUserSignUp(None, None)
    assert resultPackage[RESPONSE_STRING] == 'email null'
    assert resultPackage[RESPONSE_CODE] == 400

    resultPackage = signUpHandler.handleUserSignUp('', 'password')
    assert resultPackage[RESPONSE_STRING] == 'email empty'
    assert resultPackage[RESPONSE_CODE] == 400

    resultPackage = signUpHandler.handleUserSignUp(None, 'password')
    assert resultPackage[RESPONSE_STRING] == 'email null'
    assert resultPackage[RESPONSE_CODE] == 400

    resultPackage = signUpHandler.handleUserSignUp('email', '')
    assert resultPackage[RESPONSE_STRING] == 'password empty'
    assert resultPackage[RESPONSE_CODE] == 400

    resultPackage = signUpHandler.handleUserSignUp('email', None)
    assert resultPackage[RESPONSE_STRING] == 'password null'
    assert resultPackage[RESPONSE_CODE] == 400

    # success tests
    resultPackage = signUpHandler.handleUserSignUp('a@aol.c', '        ')
    assert resultPackage[RESPONSE_STRING] == 'signup successful'
    assert resultPackage[RESPONSE_CODE] == 201

    resultPackage = signUpHandler.handleUserSignUp('email3@m.c', '    )(*)    ')
    assert resultPackage[RESPONSE_STRING] == 'signup successful'
    assert resultPackage[RESPONSE_CODE] == 201

    resultPackage = signUpHandler.handleUserSignUp('e@mai.c', '    )(*)    ')
    assert resultPackage[RESPONSE_STRING] == 'signup successful'
    assert resultPackage[RESPONSE_CODE] == 201

    DBA.clearDatabase()

    # invalid email characters tests
    resultPackage = signUpHandler.handleUserSignUp('usern>ame', 'password')
    assert resultPackage[RESPONSE_STRING] == 'email invalid'
    assert resultPackage[RESPONSE_CODE] == 403

    resultPackage = signUpHandler.handleUserSignUp('-email', 'password')
    assert resultPackage[RESPONSE_STRING] == 'email length bad'
    assert resultPackage[RESPONSE_CODE] == 402

    resultPackage = signUpHandler.handleUserSignUp('email;', 'password')
    assert resultPackage[RESPONSE_STRING] == 'email length bad'
    assert resultPackage[RESPONSE_CODE] == 402

    resultPackage = signUpHandler.handleUserSignUp('{}{}{}{}{}', 'password')
    assert resultPackage[RESPONSE_STRING] == 'email invalid'
    assert resultPackage[RESPONSE_CODE] == 403

    resultPackage = signUpHandler.handleUserSignUp('email1', 'password')
    assert resultPackage[RESPONSE_STRING] == 'email length bad'
    assert resultPackage[RESPONSE_CODE] == 402

    resultPackage = signUpHandler.handleUserSignUp('@', 'password')
    assert resultPackage[RESPONSE_STRING] == 'email length bad'
    assert resultPackage[RESPONSE_CODE] == 402

    resultPackage = signUpHandler.handleUserSignUp('@gmail.com', 'password')
    assert resultPackage[RESPONSE_STRING] == 'email invalid'
    assert resultPackage[RESPONSE_CODE] == 403

    resultPackage = signUpHandler.handleUserSignUp('gmail.com', 'password')
    assert resultPackage[RESPONSE_STRING] == 'email invalid'
    assert resultPackage[RESPONSE_CODE] == 403

    resultPackage = signUpHandler.handleUserSignUp('robert.@', 'password')
    assert resultPackage[RESPONSE_STRING] == 'email invalid'
    assert resultPackage[RESPONSE_CODE] == 403

    resultPackage = signUpHandler.handleUserSignUp('robert@', 'password')
    assert resultPackage[RESPONSE_STRING] == 'email invalid'
    assert resultPackage[RESPONSE_CODE] == 403

    resultPackage = signUpHandler.handleUserSignUp('robert@gmail.', 'password')
    assert resultPackage[RESPONSE_STRING] == 'email invalid'
    assert resultPackage[RESPONSE_CODE] == 403

    resultPackage = signUpHandler.handleUserSignUp('(*&)@gmail.', 'password')
    assert resultPackage[RESPONSE_STRING] == 'email invalid'
    assert resultPackage[RESPONSE_CODE] == 403

    # duplicate email tests
    signUpHandler.handleUserSignUp('email@aol.com', 'password1')
    resultPackage = signUpHandler.handleUserSignUp('email@aol.com', 'password1')
    assert resultPackage[RESPONSE_STRING] == 'email already exists'
    assert resultPackage[RESPONSE_CODE] == 404

    DBA.clearDatabase()

    signUpHandler.handleUserSignUp('Email@gmail.com', 'password')
    resultPackage = signUpHandler.handleUserSignUp('Email@gmail.com', 'password')
    assert resultPackage[RESPONSE_STRING] == 'email already exists'
    assert resultPackage[RESPONSE_CODE] == 404

    resultPackage = signUpHandler.handleUserSignUp('email@gmail.com', 'password')
    assert resultPackage[RESPONSE_STRING] == 'email already exists'
    assert resultPackage[RESPONSE_CODE] == 404

    DBA.clearDatabase()

    signUpHandler.handleUserSignUp('email@gmail.com', 'password')
    resultPackage = signUpHandler.handleUserSignUp('Email@gmail.com', 'password')
    assert resultPackage[RESPONSE_STRING] == 'email already exists'
    assert resultPackage[RESPONSE_CODE] == 404

    DBA.clearDatabase()

    signUpHandler.handleUserSignUp('UsErNAME@gmail.com', 'password')
    resultPackage = signUpHandler.handleUserSignUp('USERNAME@gmail.com', 'password')
    assert resultPackage[RESPONSE_STRING] == 'email already exists'
    assert resultPackage[RESPONSE_CODE] == 404

    DBA.clearDatabase()

    signUpHandler.handleUserSignUp('USERNAME@gmail.com', 'password')
    resultPackage = signUpHandler.handleUserSignUp('username@gmail.com', 'password')
    assert resultPackage[RESPONSE_STRING] == 'email already exists'
    assert resultPackage[RESPONSE_CODE] == 404

    DBA.clearDatabase()

    # characters out of range in email or password tests
    resultPackage = signUpHandler.handleUserSignUp('testemailtestemailtestemaffdddddddddddddddddddddddasdawdawdwadwddawdawdaffffil@outlook.com', 'testemailtestemailtestemailtestemailtestemailtestu;')
    assert resultPackage[RESPONSE_STRING] == 'email length bad'
    assert resultPackage[RESPONSE_CODE] == 402

    resultPackage = signUpHandler.handleUserSignUp(',', 'testemailtestemailtestemailtestemailtestemailtestemail')
    assert resultPackage[RESPONSE_STRING] == 'email length bad'
    assert resultPackage[RESPONSE_CODE] == 402

    resultPackage = signUpHandler.handleUserSignUp('User@aol.com', '   ')
    assert resultPackage[RESPONSE_STRING] == "password length bad"
    assert resultPackage[RESPONSE_CODE] == 402

    resultPackage = signUpHandler.handleUserSignUp('Email1@aol.com', 'testemailtestemailtestemailtestemailtestemailtestu;ddddddddddddddd')
    assert resultPackage[RESPONSE_STRING] == "password length bad"
    assert resultPackage[RESPONSE_CODE] == 402

    resultPackage = signUpHandler.handleUserSignUp('Email1@aol.com', '*')
    assert resultPackage[RESPONSE_STRING] == "password length bad"
    assert resultPackage[RESPONSE_CODE] == 402

    resultPackage = signUpHandler.handleUserSignUp('Email2@aol.com', ' ')
    assert resultPackage[RESPONSE_STRING] == "password length bad"
    assert resultPackage[RESPONSE_CODE] == 402

    resultPackage = signUpHandler.handleUserSignUp('GoodEmail@aol.com', 'GoodPassword123')
    assert resultPackage[RESPONSE_STRING] == 'signup successful'
    assert resultPackage[RESPONSE_CODE] == 201

    DBA.clearDatabase()
    DBA.closeConnection()

def test_getUser():
    DBA.createConnection()
    user = signUpHandler.getUser('email1@aol.com', 'password1')
    assert user.getEmail() == 'email1@aol.com'
    assert user.getTextPassword() == 'password1'
    assert user.getHashedPassword() != None
    assert user.getUserId() != None
    assert len(user.getUserId()) == 36

    del user
    DBA.clearDatabase()
    DBA.closeConnection()
