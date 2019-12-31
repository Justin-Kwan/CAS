import pytest
import sys
import os

THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
sys.path.append(THIS_FOLDER + '/../src/DatabaseLayer')
sys.path.append(THIS_FOLDER + '/../src/BusinessLayer/handlers')

from SignUpHandler import SignUpHandler
from DatabaseAccessor import DatabaseAccessor

signUpHandler = SignUpHandler()
DBA = DatabaseAccessor()

def getUser(email, textPassword):
    user = User(email, textPassword)
    user.encryptAndSetPassword()
    user.generateAndUpdateUserId()
    return user

def test_handleUserSignUp():
    DBA.createConnection()
    DBA.clearDatabase()

    # empty field(s) tests
    response = signUpHandler.handleUserSignUp('', '')
    assert response['response string'] == 'email empty'
    assert response['response code'] == 400

    response = signUpHandler.handleUserSignUp(None, None)
    assert response['response string'] == 'email null'
    assert response['response code'] == 400

    response = signUpHandler.handleUserSignUp('', 'password')
    assert response['response string'] == 'email empty'
    assert response['response code'] == 400

    response = signUpHandler.handleUserSignUp(None, 'password')
    assert response['response string'] == 'email null'
    assert response['response code'] == 400

    response = signUpHandler.handleUserSignUp('email', '')
    assert response['response string'] == 'password empty'
    assert response['response code'] == 400

    response = signUpHandler.handleUserSignUp('email', None)
    assert response['response string'] == 'password null'
    assert response['response code'] == 400

    # success tests
    response = signUpHandler.handleUserSignUp('email3@gmail.ca', '    )(*)    ')
    assert response['response string'] == 'signup successful'
    assert response['response code'] == 201

    response = signUpHandler.handleUserSignUp('e@mai.c', '    )(*)    ')
    assert response['response string'] == 'signup successful'
    assert response['response code'] == 201

    response = signUpHandler.handleUserSignUp('hello@aol.c', '        ')
    assert response['response string'] == 'signup successful'
    assert response['response code'] == 201

    response = signUpHandler.handleUserSignUp('email3@m.ca', '    )(*)    ')
    assert response['response string'] == 'signup successful'
    assert response['response code'] == 201

    DBA.clearDatabase()

    # invalid email characters tests
    response = signUpHandler.handleUserSignUp('usern>ame', 'password')
    assert response['response string'] == 'email invalid'
    assert response['response code'] == 403

    response = signUpHandler.handleUserSignUp('-email', 'password')
    assert response['response string'] == 'email length bad'
    assert response['response code'] == 402

    response = signUpHandler.handleUserSignUp('email;', 'password')
    assert response['response string'] == 'email length bad'
    assert response['response code'] == 402

    response = signUpHandler.handleUserSignUp('{}{}{}{}{}', 'password')
    assert response['response string'] == 'email invalid'
    assert response['response code'] == 403

    response = signUpHandler.handleUserSignUp('email1', 'password')
    assert response['response string'] == 'email length bad'
    assert response['response code'] == 402

    response = signUpHandler.handleUserSignUp('@', 'password')
    assert response['response string'] == 'email length bad'
    assert response['response code'] == 402

    response = signUpHandler.handleUserSignUp('@gmail.com', 'password')
    assert response['response string'] == 'email invalid'
    assert response['response code'] == 403

    response = signUpHandler.handleUserSignUp('gmail.com', 'password')
    assert response['response string'] == 'email invalid'
    assert response['response code'] == 403

    response = signUpHandler.handleUserSignUp('robert.@', 'password')
    assert response['response string'] == 'email invalid'
    assert response['response code'] == 403

    response = signUpHandler.handleUserSignUp('robert@', 'password')
    assert response['response string'] == 'email invalid'
    assert response['response code'] == 403

    response = signUpHandler.handleUserSignUp('robert@gmail.', 'password')
    assert response['response string'] == 'email invalid'
    assert response['response code'] == 403

    response = signUpHandler.handleUserSignUp('(*&)@gmail.', 'password')
    assert response['response string'] == 'email invalid'
    assert response['response code'] == 403

    # duplicate email tests
    signUpHandler.handleUserSignUp('email@aol.com', 'password1')
    response = signUpHandler.handleUserSignUp('email@aol.com', 'password1')
    assert response['response string'] == 'email already exists'
    assert response['response code'] == 404

    DBA.clearDatabase()

    signUpHandler.handleUserSignUp('Email@gmail.com', 'password')
    response = signUpHandler.handleUserSignUp('Email@gmail.com', 'password')
    assert response['response string'] == 'email already exists'
    assert response['response code'] == 404

    response = signUpHandler.handleUserSignUp('email@gmail.com', 'password')
    assert response['response string'] == 'email already exists'
    assert response['response code'] == 404

    DBA.clearDatabase()

    signUpHandler.handleUserSignUp('email@gmail.com', 'password')
    response = signUpHandler.handleUserSignUp('Email@gmail.com', 'password')
    assert response['response string'] == 'email already exists'
    assert response['response code'] == 404

    DBA.clearDatabase()

    signUpHandler.handleUserSignUp('UsErNAME@gmail.com', 'password')
    response = signUpHandler.handleUserSignUp('USERNAME@gmail.com', 'password')
    assert response['response string'] == 'email already exists'
    assert response['response code'] == 404

    DBA.clearDatabase()

    signUpHandler.handleUserSignUp('USERNAME@gmail.com', 'password')
    response = signUpHandler.handleUserSignUp('username@gmail.com', 'password')
    assert response['response string'] == 'email already exists'
    assert response['response code'] == 404

    DBA.clearDatabase()

    # characters out of range in email or password tests
    response = signUpHandler.handleUserSignUp('testemailtestemailtestemaffdddddddddddddddddddddddasdawdawdwadwddawdawdaffffil@outlook.com', 'testemailtestemailtestemailtestemailtestemailtestu;')
    assert response['response string'] == 'email length bad'
    assert response['response code'] == 402

    response = signUpHandler.handleUserSignUp(',', 'testemailtestemailtestemailtestemailtestemailtestemail')
    assert response['response string'] == 'email length bad'
    assert response['response code'] == 402

    response = signUpHandler.handleUserSignUp('User@aol.com', '   ')
    assert response['response string'] == "password length bad"
    assert response['response code'] == 402

    response = signUpHandler.handleUserSignUp('Email1@aol.com', 'testemailtestemailtestemailtestemailtestemailtestu;ddddddddddddddd')
    assert response['response string'] == "password length bad"
    assert response['response code'] == 402

    response = signUpHandler.handleUserSignUp('Email1@aol.com', '*')
    assert response['response string'] == "password length bad"
    assert response['response code'] == 402

    response = signUpHandler.handleUserSignUp('Email2@aol.com', ' ')
    assert response['response string'] == "password length bad"
    assert response['response code'] == 402

    response = signUpHandler.handleUserSignUp('GoodEmail@aol.com', 'GoodPassword123')
    assert response['response string'] == 'signup successful'
    assert response['response code'] == 201

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
