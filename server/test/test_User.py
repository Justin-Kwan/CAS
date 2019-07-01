import pytest
import sys
sys.path.append('/Users/justinkwan/Documents/WebApps/UserAuth/server/src')
from User import User

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

def test_encryptAndUpdatePassword():
    user = User('username5', 'password5')
    user.encryptAndUpdatePassword('password5')
    assert user.getHashedPassword() != None

    del user
