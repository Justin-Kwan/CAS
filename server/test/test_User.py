import pytest
import sys
sys.path.append('/Users/justinkwan/Documents/WebApps/UserAuth/server/src')
from User import User
import jwt

def test_getUsername():
    user = User('username1', 'password1')
    assert user.getUsername() == 'username1'

    del user

def test_getTextPassword():
    user = User('username2', 'password2')
    assert user.getTextPassword() == 'password2'

    del user

def test_getHashedPassword():
    user = User('username3', 'password3')
    user.encryptAndUpdatePassword('password3')
    assert user.getHashedPassword() != None

    del user

def test_getUserId():
    user = User('username4', 'password4')
    assert user.getUserId() != None
    assert len(user.getUserId()) == 36

    del user

def test_getSecurityToken():
    user = User('username5', 'password5')
    user.generateAndUpdateSecurityToken()
    securityToken = user.getSecurityToken()

    assert securityToken != None
    
    userData = jwt.decode(securityToken, 'fake_secret_key', algorithms=['HS256'])

    assert 'username' in userData
    assert 'username5' in userData.values()
    assert 'user id' in userData

def test_encryptAndUpdatePassword():
    user = User('username6', 'password6')
    user.encryptAndUpdatePassword('password6')
    assert user.getHashedPassword() != None

    del user

def test_generateAndUpdateSecurityToken():
    user = User('username7', 'password7')
    user.generateAndUpdateSecurityToken()
    securityToken = user.getSecurityToken()

    userData = jwt.decode(securityToken, 'fake_secret_key', algorithms=['HS256'])

    assert 'username' in userData
    assert 'username7' in userData.values()
    assert 'user id' in userData
