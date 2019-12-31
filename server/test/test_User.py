import pytest
import sys
import os

THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
sys.path.append(THIS_FOLDER + '/../src/BusinessLayer/models')

from User import User
import jwt

def getUser(email, textPassword):
    user = User(email, textPassword)
    user.encryptAndSetPassword()
    user.generateAndSetUserId()
    return user

def test_getEmail():
    user = getUser('email1@aol.com', 'password1')
    assert user.getEmail() == 'email1@aol.com'
    del user

def test_getTextPassword():
    user = getUser('email2@aol.com', 'password2')
    assert user.getTextPassword() == 'password2'
    del user

def test_getHashedPassword():
    user = getUser('email3@aol.com', 'password3')
    assert user.getHashedPassword() != None
    del user

def test_getUserId():
    user = getUser('email4@aol.com', 'password4')
    assert user.getUserId() != None
    assert len(user.getUserId()) == 36
    del user

def test_setUserId():
    user = getUser('email8@aol.com', 'password8')
    user.setUserId('#123')
    assert user.getUserId() == '#123'
    del user

    user = getUser('email9@aol.com', 'password9')
    user.setUserId(123)
    assert user.getUserId() == 123
    del user

def test_setAuthToken():
    user = getUser('email8@aol.com', 'password8')
    user.setAuthToken('#123')
    assert user.getAuthToken() == '#123'
    del user

    user = getUser('email9@aol.com', 'password9')
    user.setAuthToken(123)
    assert user.getAuthToken() == 123
    del user

def test_generateAndSetUserId():
    user = getUser('email10@aol.com', 'password10')
    user.generateAndSetUserId()
    assert user.getUserId() != None
    assert len(user.getUserId()) == 36

def test_getAuthToken():
    user = getUser('email5@aol.com', 'password5')
    user.generateAndSetAuthToken()
    authToken = user.getAuthToken()

    assert authToken != None

    userData = jwt.decode(authToken, 'fake_secret_key', algorithms=['HS256'])

    assert 'email' in userData
    assert 'email5@aol.com' in userData.values()
    assert 'user id' in userData
    assert user.getUserId() in userData.values()

def test_encryptAndSetPassword():
    user = getUser('email6@aol.com', 'password6')
    user.encryptAndSetPassword()
    assert user.getHashedPassword() != None
    del user

def test_generateAndSetAuthToken():
    user = getUser('email7@aol.com', 'password7')
    user.generateAndSetAuthToken()
    authToken = user.getAuthToken()

    userData = jwt.decode(authToken, 'fake_secret_key', algorithms=['HS256'])

    assert 'email' in userData
    assert 'email7@aol.com' in userData.values()
    assert 'user id' in userData
    assert user.getUserId() in userData.values()
