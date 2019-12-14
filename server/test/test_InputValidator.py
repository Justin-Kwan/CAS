import pytest
import sys
sys.path.append('/Users/justinkwan/Documents/WebApps/UserAuth/server/src/BusinessLayer/handlers')
sys.path.append('/Users/justinkwan/Documents/WebApps/UserAuth/server/src/BusinessLayer/models')
sys.path.append('/Users/justinkwan/Documents/WebApps/UserAuth/server/src/BusinessLayer')
sys.path.append('/Users/justinkwan/Documents/WebApps/UserAuth/server/src/DataBaseLayer')
from InputValidator   import InputValidator
from DatabaseAccessor import DatabaseAccessor
from User             import User

inputValidator = InputValidator()
DBA = DatabaseAccessor()

def getUser(username, password):
    user = User(username, password)
    user.encryptAndSetPassword(password)
    user.generateAndSetUserId()
    return user

def test_checkInputNull():
    assert inputValidator.checkInputNull(None, None) == "username null"
    assert inputValidator.checkInputNull(None, 'password123') == "username null"
    assert inputValidator.checkInputNull('username123', None) == "password null"
    assert inputValidator.checkInputNull('username123', 'password123') == "username & password not null"
    assert inputValidator.checkInputNull('', '') == "username & password not null"

def test_checkInputEmpty():
    user = getUser('', '')
    assert inputValidator.checkInputEmpty(user) == "username empty"
    del user

    user = getUser('', 'password')
    assert inputValidator.checkInputEmpty(user) == 'username empty'
    del user

    user = getUser('username', '')
    assert inputValidator.checkInputEmpty(user) == 'password empty'
    del user

    user = getUser('username', 'password')
    assert inputValidator.checkInputEmpty(user) == 'username & password not empty'
    del user

def test_checkInputLength():
    user = getUser('NewUser123', 'testusername')
    assert inputValidator.checkInputLength(user) == 'username & password length ok'
    del user

    user = getUser('usrnmm', 'testusernametestusernametestusernam')
    assert inputValidator.checkInputLength(user) == 'username & password length ok'
    del user

    user = getUser('testusernametestusernametestusername', 'testusernametestusernametestusernametestusernametestusernametestu;')
    assert inputValidator.checkInputLength(user) == "username length bad"
    del user

    user = getUser('', 'usrnmdd')
    assert inputValidator.checkInputLength(user) == "username length bad"
    del user

    user = getUser('User', '')
    assert inputValidator.checkInputLength(user) == "username length bad"
    del user

    user = getUser(',', 'testusernametestusernametestusernametestusernametestusernametestusername')
    assert inputValidator.checkInputLength(user) == "username length bad"
    del user

    user = getUser('usrnmm', 'testusernametestusernametestusernametestusernametestusernametestu')
    assert inputValidator.checkInputLength(user) == 'username & password length ok'
    del user

    user = getUser('usrnmm', 'testusernametestusernametestusernametestusernametestusernametestus')
    assert inputValidator.checkInputLength(user) == "password length bad"
    del user

    user = getUser('usrnmm', 'passwor')
    assert inputValidator.checkInputLength(user) == "password length bad"
    del user

def test_isUsernameCharsOk():
    user = getUser('string2', 'password123')
    assert inputValidator.isUsernameCharsOk(user) == True
    del user

    user = getUser('fake$username)', 'password123')
    assert inputValidator.isUsernameCharsOk(user) == False
    del user

    user = getUser(')(*&^)', 'password123')
    assert inputValidator.isUsernameCharsOk(user) == False
    del user

    user = getUser(')(*&^)textTest*&^%moretestis*fun;:', 'password123')
    assert inputValidator.isUsernameCharsOk(user) == False
    del user

def test_isPasswordCorrect():
    DBA.createConnection()

    user1 = getUser('username1', 'password1')
    DBA.insertUserInfo(user1)
    user2 = getUser('username1', 'password1')
    selectedHashedPassword = DBA.selectHashedPassword(user2).encode('utf-8')
    isPasswordCorrect = inputValidator.isPasswordCorrect(user2, selectedHashedPassword)
    assert isPasswordCorrect == True

    del user1
    del user2
    DBA.clearDatabase()

    user1 = getUser('username2', 'password2')
    DBA.insertUserInfo(user1)
    user2 = getUser('username2', 'password1')
    selectedHashedPassword = DBA.selectHashedPassword(user2).encode('utf-8')
    isPasswordCorrect = inputValidator.isPasswordCorrect(user2, selectedHashedPassword)
    assert isPasswordCorrect == False

    del user1
    del user2
    DBA.clearDatabase()

    user1 = getUser('username3', '^&*()()')
    DBA.insertUserInfo(user1)
    user2 = getUser('username3', '^&*()()')
    selectedHashedPassword = DBA.selectHashedPassword(user2).encode('utf-8')
    isPasswordCorrect = inputValidator.isPasswordCorrect(user2, selectedHashedPassword)
    assert isPasswordCorrect == True

    del user1
    del user2
    DBA.clearDatabase()
    DBA.closeConnection()
