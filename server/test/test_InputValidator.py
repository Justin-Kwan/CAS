import pytest
import sys
import os

THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
sys.path.append(THIS_FOLDER + '/../src/database-layer')
sys.path.append(THIS_FOLDER + '/../src/domain-layer/utilities')
sys.path.append(THIS_FOLDER + '/../src/domain-layer/models')
sys.path.append(THIS_FOLDER + '/../src/domain-layer/handlers')

from InputValidator   import InputValidator
from DatabaseAccessor import DatabaseAccessor
from User             import User

inputValidator = InputValidator()
DBA = DatabaseAccessor()

def getUser(email, textPassword):
    user = User(email, textPassword)
    user.encryptAndSetPassword()
    user.generateAndSetUserId()
    return user

def test_checkInputNull():
    assert inputValidator.checkInputNull(None, None) == "email null"
    assert inputValidator.checkInputNull(None, 'password123') == "email null"
    assert inputValidator.checkInputNull('email123', None) == "password null"
    assert inputValidator.checkInputNull('email123', 'password123') == "email & password not null"
    assert inputValidator.checkInputNull('', '') == "email & password not null"

def test_checkInputEmpty():
    user = getUser('', '')
    assert inputValidator.checkInputEmpty(user) == "email empty"
    del user

    user = getUser('', 'password')
    assert inputValidator.checkInputEmpty(user) == 'email empty'
    del user

    user = getUser('email', '')
    assert inputValidator.checkInputEmpty(user) == 'password empty'
    del user

    user = getUser('email', 'password')
    assert inputValidator.checkInputEmpty(user) == 'email & password not empty'
    del user

def test_checkInputLength():
    user = getUser('NewUser123', 'testemail')
    assert inputValidator.checkInputLength(user, 'email') == 'email length ok'
    del user

    user = getUser('NewUser123', 'testemail')
    assert inputValidator.checkInputLength(user, 'password') == 'password length ok'
    del user

    user = getUser('usrnmmm', 'testemailtestemailtestusernam')
    assert inputValidator.checkInputLength(user, 'email') == 'email length ok'
    del user

    user = getUser('usrnmmm', 'testemailtestemailtestusernam')
    assert inputValidator.checkInputLength(user, 'password') == 'password length ok'
    del user

    user = getUser('testemailtestemailtestemail', 'testemailtestemailtestemailtestemailtestemailtestu;')
    assert inputValidator.checkInputLength(user, 'email') == "email length ok"
    del user

    user = getUser('testemailtestemailtestemail', 'testemailtestemailtestemailtestemailtestemailtestu;')
    assert inputValidator.checkInputLength(user, 'password') == "password length ok"
    del user

    user = getUser('eightyninechars__________________________________________________________________________', 'testemailtestemailtestemailtestemailtestemailtestu;')
    assert inputValidator.checkInputLength(user, 'email') == "email length ok"
    del user

    user = getUser('user', 'sixtyfivechars___________________________________________________')
    assert inputValidator.checkInputLength(user, 'password') == "password length ok"
    del user

    user = getUser('', 'usrnmdd')
    assert inputValidator.checkInputLength(user, 'email') == "email length bad"
    del user

    user = getUser('', 'usrnmdd')
    assert inputValidator.checkInputLength(user, 'password') == "password length bad"
    del user

    user = getUser('User', '')
    assert inputValidator.checkInputLength(user, 'email') == "email length bad"
    del user

    user = getUser('User', '')
    assert inputValidator.checkInputLength(user, 'password') == "password length bad"
    del user

    user = getUser('ninetychars_______________________________________________________________________________', 'sixtyfivechars___________________________________________________')
    assert inputValidator.checkInputLength(user, 'email') == "email length bad"
    del user

    user = getUser('User', 'sixtysixchars_____________________________________________________')
    assert inputValidator.checkInputLength(user, 'password') == "password length bad"
    del user

    user = getUser(',', 'testemailtestemailtestemailtestemailtestemailtestemail')
    assert inputValidator.checkInputLength(user, 'password') == "password length ok"
    del user

    user = getUser('u@ol.c', 'testemailtestemailtestemailtestemailtestemailtestu')
    assert inputValidator.checkInputLength(user, 'email') == 'email length bad'
    del user

    user = getUser('u@ol.ca', 'testemailtestemailtestemailtestemailtestemailtestusffffffffffffff')
    assert inputValidator.checkInputLength(user, 'email') == "email length ok"
    del user

def test_isEmailCharsOk():
    user = getUser('string2@gmail.com', 'password123')
    assert inputValidator.isEmailCharsOk(user) == True
    del user

    user = getUser("username", 'password123')
    assert inputValidator.isEmailCharsOk(user) == False
    del user

    user = getUser('string2', 'password123')
    assert inputValidator.isEmailCharsOk(user) == False
    del user

    user = getUser('robert@gmail', 'password123')
    assert inputValidator.isEmailCharsOk(user) == False
    del user

    user = getUser('email3@gmail.com', 'password123')
    assert inputValidator.isEmailCharsOk(user) == True
    del user

    user = getUser('fake$email)', 'password123')
    assert inputValidator.isEmailCharsOk(user) == False
    del user

    user = getUser(')(*&^)@gmail.com', 'password123')
    assert inputValidator.isEmailCharsOk(user) == False
    del user

    user = getUser(')(*&^)textTest*&^%moretestis*fun;:', 'password123')
    assert inputValidator.isEmailCharsOk(user) == False
    del user

    user = getUser('email1@aol.com', 'password1')
    assert inputValidator.isEmailCharsOk(user) == True

    user = getUser('u@gmail.com', 'password1')
    assert inputValidator.isEmailCharsOk(user) == True

    user = getUser('@gmail.com', 'password1')
    assert inputValidator.isEmailCharsOk(user) == False

    user = getUser('a@aol.c', 'password1')
    assert inputValidator.isEmailCharsOk(user) == True

    user = getUser('a@aol.ca', 'password1')
    assert inputValidator.isEmailCharsOk(user) == True

    user = getUser('robertwang%@gmail.com', 'password1')
    assert inputValidator.isEmailCharsOk(user) == True

    user = getUser('robertwanggmail.com', 'password1')
    assert inputValidator.isEmailCharsOk(user) == False

    user = getUser('robertwang@', 'password1')
    assert inputValidator.isEmailCharsOk(user) == False

    user = getUser('robertwang.com', 'password1')
    assert inputValidator.isEmailCharsOk(user) == False

    user = getUser('robert_wang@yahoo.com', 'password1')
    assert inputValidator.isEmailCharsOk(user) == True

    user = getUser('robert+wang@yahoo.com', 'password1')
    assert inputValidator.isEmailCharsOk(user) == True

    user = getUser('_robertwang@yahoo.com', 'password1')
    assert inputValidator.isEmailCharsOk(user) == True

    user = getUser('robertwang_@yahoo.com', 'password1')
    assert inputValidator.isEmailCharsOk(user) == True

    user = getUser('r@yahoo.com', 'password1')
    assert inputValidator.isEmailCharsOk(user) == True

    user = getUser('_@yahoo.com', 'password1')
    assert inputValidator.isEmailCharsOk(user) == True


def test_isPasswordCorrect():
    DBA.createConnection()

    user1 = getUser('email1', 'password1')
    DBA.insertUserInfo(user1)
    user2 = getUser('email1', 'password1')
    selectedHashedPassword = DBA.selectHashedPassword(user2).encode('utf-8')
    isPasswordCorrect = inputValidator.isPasswordCorrect(user2, selectedHashedPassword)
    assert isPasswordCorrect == True

    del user1
    del user2
    DBA.clearDatabase()

    user1 = getUser('email2', 'password2')
    DBA.insertUserInfo(user1)
    user2 = getUser('email2', 'password1')
    selectedHashedPassword = DBA.selectHashedPassword(user2).encode('utf-8')
    isPasswordCorrect = inputValidator.isPasswordCorrect(user2, selectedHashedPassword)
    assert isPasswordCorrect == False

    del user1
    del user2
    DBA.clearDatabase()

    user1 = getUser('email3', '^&*()()')
    DBA.insertUserInfo(user1)
    user2 = getUser('email3', '^&*()()')
    selectedHashedPassword = DBA.selectHashedPassword(user2).encode('utf-8')
    isPasswordCorrect = inputValidator.isPasswordCorrect(user2, selectedHashedPassword)
    assert isPasswordCorrect == True

    del user1
    del user2
    DBA.clearDatabase()
    DBA.closeConnection()
