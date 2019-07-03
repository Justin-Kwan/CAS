import pytest
import sys
sys.path.append('/Users/justinkwan/Documents/WebApps/UserAuth/server/src')
from User import User
import jwt

def getUser(username, password):
    user = User(username, password)
    user.encryptAndUpdatePassword(password)
    user.generateAndUpdateUserId()
    return user

def test_getUsername():
    user = getUser('username1', 'password1')
    assert user.getUsername() == 'username1'
    del user

def test_getTextPassword():
    user = getUser('username2', 'password2')
    assert user.getTextPassword() == 'password2'
    del user

def test_getHashedPassword():
    user = getUser('username3', 'password3')
    assert user.getHashedPassword() != None
    del user

def test_getUserId():
    user = getUser('username4', 'password4')
    assert user.getUserId() != None
    assert len(user.getUserId()) == 36
    del user

def test_updateUserId():
    user = getUser('username8', 'password8')
    user.updateUserId('#123')
    assert user.getUserId() == '#123'
    del user

    user = getUser('username9', 'password9')
    user.updateUserId(123)
    assert user.getUserId() == 123
    del user

def test_generateAndUpdateUserId():
    user = getUser('username10', 'password10')
    user.generateAndUpdateUserId()
    assert user.getUserId() != None
    assert len(user.getUserId()) == 36

def test_getSecurityToken():
    user = getUser('username5', 'password5')
    user.generateAndUpdateSecurityToken()
    securityToken = user.getSecurityToken()

    assert securityToken != None
    
    userData = jwt.decode(securityToken, 'fake_secret_key', algorithms=['HS256'])

    assert 'username' in userData
    assert 'username5' in userData.values()
    assert 'user id' in userData

def test_encryptAndUpdatePassword():
    user = getUser('username6', 'password6')
    assert user.getHashedPassword() != None
    del user

def test_generateAndUpdateSecurityToken():
    user = getUser('username7', 'password7')
    user.generateAndUpdateSecurityToken()
    securityToken = user.getSecurityToken()

    userData = jwt.decode(securityToken, 'fake_secret_key', algorithms=['HS256'])

    assert 'username' in userData
    assert 'username7' in userData.values()
    assert 'user id' in userData
