import pytest
import sys
import os

THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
sys.path.append(THIS_FOLDER + '/../src/database-layer')
sys.path.append(THIS_FOLDER + '/../src/domain-layer/handlers')
sys.path.append(THIS_FOLDER + '/../src/domain-layer/models')
sys.path.append(THIS_FOLDER + '/../src/domain-layer/utilities')

from DatabaseAccessor import DatabaseAccessor
from InputValidator   import InputValidator
from User             import User

inputValidator = InputValidator()
DBA = DatabaseAccessor()

def getUser(email, textPassword, userId):
    user = User(email, textPassword)
    user.encryptAndSetPassword()
    user.setUserId(userId)
    return user

def test_insertUserInfo():
    DBA.createConnection()
    DBA.clearDatabase()

    user = getUser('testEmail1', 'testPassword1', 'testId1')
    DBA.insertUserInfo(user)
    selectedEmail = DBA.selectEmail(user)
    selectedHashedPassword = DBA.selectHashedPassword(user)
    selectedUserId = DBA.selectUserIdFromEmail(user)
    assert selectedEmail == 'testEmail1'
    assert selectedHashedPassword != None
    assert selectedUserId == 'testId1'

    del user
    DBA.clearDatabase()

    user = getUser('09812', '*7%-', 'testId2')
    DBA.insertUserInfo(user)
    selectedEmail = DBA.selectEmail(user)
    selectedHashedPassword = DBA.selectHashedPassword(user)
    selectedUserId = DBA.selectUserIdFromEmail(user)
    assert selectedEmail == '09812'
    assert selectedHashedPassword != None
    assert selectedUserId == 'testId2'

    del user
    DBA.clearDatabase()

    user = getUser('-l-&$', '=testpassw0rd', 'testId3')
    DBA.insertUserInfo(user)
    selectedEmail = DBA.selectEmail(user)
    selectedHashedPassword = DBA.selectHashedPassword(user)
    selectedUserId = DBA.selectUserIdFromEmail(user)
    assert selectedEmail == '-l-&$'
    assert selectedHashedPassword != None
    assert selectedUserId == 'testId3'

    del user
    DBA.clearDatabase()

    user = getUser('fake-user', 'password123', '')
    user.generateAndSetUserId()
    DBA.insertUserInfo(user)
    selectedEmail = DBA.selectEmail(user)
    selectedHashedPassword = DBA.selectHashedPassword(user)
    selectedUserId = DBA.selectUserIdFromEmail(user)
    assert selectedEmail == 'fake-user'
    assert selectedHashedPassword != None
    assert selectedUserId == user.getUserId()

    del user
    DBA.clearDatabase()
    DBA.closeConnection()

def test_updatePassword():
    DBA.createConnection()
    DBA.clearDatabase()

    user = getUser('test_email@aol.com', 'test_password', 'test_id')
    DBA.insertUserInfo(user)
    user.hashedPassword = 'new_test_hashed_password'
    DBA.updatePassword(user)
    updatedPassword = DBA.selectHashedPassword(user)
    assert updatedPassword == 'new_test_hashed_password'

    del user

    user = getUser('test_email_2@aol.com', 'test_password_2', 'test_id_2')
    DBA.insertUserInfo(user)
    user.hashedPassword = 'new_test_hashed_password_2'
    DBA.updatePassword(user)
    updatedPassword = DBA.selectHashedPassword(user)
    assert updatedPassword == 'new_test_hashed_password_2'

    del user

    user = getUser('test_email_3@aol.com', 'test_password_3', 'test_id_3')
    DBA.insertUserInfo(user)
    user.hashedPassword = 'new_test_hashed_password_3'
    DBA.updatePassword(user)
    updatedPassword = DBA.selectHashedPassword(user)
    assert updatedPassword == 'new_test_hashed_password_3'

    del user
    DBA.clearDatabase()
    DBA.closeConnection()

def test_selectEmail():
    DBA.createConnection()
    DBA.clearDatabase()

    user1 = getUser('testEmail1', 'testPassword1', 'testId')
    user2 = getUser('testEmail2', 'testPassword2', 'testId')
    user3 = getUser('testEmail3', 'testPassword3', 'testId')
    DBA.insertUserInfo(user1)
    DBA.insertUserInfo(user2)
    DBA.insertUserInfo(user3)
    selectedEmail = DBA.selectEmail(user2)
    assert selectedEmail == 'testEmail2'

    del user1
    del user2
    del user3
    DBA.clearDatabase()

    user1 = getUser('fakename', 'teddddstPassword1', 'testId')
    user2 = getUser('testdwdadEmail2', 'testPawddassword2', 'testId')
    user3 = getUser('w90', 'test', 'testId')
    DBA.insertUserInfo(user1)
    DBA.insertUserInfo(user2)
    DBA.insertUserInfo(user3)
    selectedEmail = DBA.selectEmail(user3)
    assert selectedEmail == 'w90'

    del user1
    del user2
    del user3
    DBA.clearDatabase()
    DBA.closeConnection()

# test password selecting function
def test_selectHashedPassword():
    DBA.createConnection()
    DBA.clearDatabase()

    user1 = getUser('rando', 'testPassword1', 'testId')
    user2 = getUser('rando2', 'testPassword2', 'testId')
    user3 = getUser('rando3', 'testPassword3', 'testId')
    DBA.insertUserInfo(user1)
    DBA.insertUserInfo(user2)
    DBA.insertUserInfo(user3)
    selectedHashedPassword = DBA.selectHashedPassword(user2)
    assert selectedHashedPassword != None

    del user1
    del user2
    del user3
    DBA.clearDatabase()

    user1 = getUser('name1', 'teddddstPassword1', 'testId')
    user2 = getUser('name2', 'testPawddassword2', 'testId')
    user3 = getUser('name3', 'test', 'testId')
    DBA.insertUserInfo(user1)
    DBA.insertUserInfo(user2)
    DBA.insertUserInfo(user3)
    selectedHashedPassword = DBA.selectHashedPassword(user3)
    assert selectedHashedPassword != None

    del user1
    del user2
    del user3
    DBA.clearDatabase()
    DBA.closeConnection()

# test user id selecting function based on given email
def test_selectUserIdFromEmail():
    DBA.createConnection()
    DBA.clearDatabase()

    user1 = getUser('name1', 'teddddstPassword1', 'testId1')
    user2 = getUser('name2', 'teddddstPassword2', 'testId2')
    user3 = getUser('name3', 'teddddstPassword3', 'testId3')
    DBA.insertUserInfo(user1)
    DBA.insertUserInfo(user2)
    DBA.insertUserInfo(user3)
    selectedUserId = DBA.selectUserIdFromEmail(user3)
    assert selectedUserId == 'testId3'

    del user1
    del user2
    del user3
    DBA.clearDatabase()

    user1 = getUser('name1', 'teddddstPassword1', 'testId0')
    user2 = getUser('name2', 'teddddstPassword2', 'testId4')
    user3 = getUser('name3', 'teddddstPassword3', 'testId9')
    DBA.insertUserInfo(user1)
    DBA.insertUserInfo(user2)
    DBA.insertUserInfo(user3)
    selectedUserId = DBA.selectUserIdFromEmail(user2)
    assert selectedUserId == 'testId4'

    del user1
    del user2
    del user3
    DBA.clearDatabase()
    DBA.closeConnection()

# test user id selecting function
def test_selectUserId():
    DBA.createConnection()
    DBA.clearDatabase()

    user1 = getUser('name1', 'teddddstPassword1', 'testId1')
    user2 = getUser('name2', 'teddddstPassword2', 'testId2')
    user3 = getUser('name3', 'teddddstPassword3', 'testId3')
    DBA.insertUserInfo(user1)
    DBA.insertUserInfo(user2)
    DBA.insertUserInfo(user3)
    selectedUserId = DBA.selectUserId(user3)
    assert selectedUserId == 'testId3'

    del user1
    del user2
    del user3
    DBA.clearDatabase()

    user1 = getUser('name1', 'teddddstPassword1', 'testId0')
    user2 = getUser('name2', 'teddddstPassword2', 'testId4')
    user3 = getUser('name3', 'teddddstPassword3', 'testId9')
    DBA.insertUserInfo(user1)
    DBA.insertUserInfo(user2)
    DBA.insertUserInfo(user3)
    selectedUserId = DBA.selectUserId(user2)
    assert selectedUserId == 'testId4'

    del user1
    del user2
    del user3
    DBA.clearDatabase()
    DBA.closeConnection()

def test_doesEmailExist():
    DBA.createConnection()
    DBA.clearDatabase()

    user1 = getUser('randomename1', 'teddddstPassword1', 'fakeid1')
    user2 = getUser('anotherrand0mName', 'testPawddassword2', 'fakeid2')
    user3 = getUser('09876543', 'test', 'fakeid3')
    user4 = getUser('09876543', 'test', 'fakeid4')
    DBA.insertUserInfo(user1)
    DBA.insertUserInfo(user2)
    DBA.insertUserInfo(user3)
    doesEmailExist = DBA.doesEmailExist(user4)
    assert doesEmailExist == True

    del user1
    del user2
    del user3
    del user4
    DBA.clearDatabase()

    user1 = getUser('robertH', 'teddddstPassword1', 'fakeid1')
    user2 = getUser('william', 'testPawddassword2', 'fakeid2')
    user3 = getUser('Johnathan', 'test', 'fakeid3')
    user4 = getUser('robertH', 'test', 'fakeid4')
    DBA.insertUserInfo(user1)
    DBA.insertUserInfo(user2)
    DBA.insertUserInfo(user3)
    doesEmailExist = DBA.doesEmailExist(user4)
    assert doesEmailExist == True

    del user1
    del user2
    del user3
    del user4
    DBA.clearDatabase()

    user1 = getUser('001', 'teddddstPassword1', 'fakeid1')
    user2 = getUser('02000000009', 'testPawddassword2', 'fakeid2')
    user3 = getUser('joe', 'test', 'fakeid3')
    user4 = getUser('uniqueName', 'password123', 'fakeid4')
    DBA.insertUserInfo(user1)
    DBA.insertUserInfo(user2)
    DBA.insertUserInfo(user3)
    doesEmailExist = DBA.doesEmailExist(user4)
    assert doesEmailExist == False

    del user1
    del user2
    del user3
    del user4
    DBA.clearDatabase()
    DBA.closeConnection()


def test_doesUserIdExist():
    DBA.createConnection()
    DBA.clearDatabase()

    user1 = getUser('randomename1', 'teddddstPassword1', 'fakeid1')
    user2 = getUser('anotherrand0mName', 'testPawddassword2', 'fakeid2')
    user3 = getUser('09876543', 'test', 'fakeid')
    user4 = getUser('09876543', 'test', 'fakeid')
    DBA.insertUserInfo(user1)
    DBA.insertUserInfo(user2)
    DBA.insertUserInfo(user3)
    doesUserIdExist = DBA.doesUserIdExist(user4)
    assert doesUserIdExist == True

    del user1
    del user2
    del user3
    del user4
    DBA.clearDatabase()

    user1 = getUser('robertH', 'testPassword1', 'fakeid1')
    user2 = getUser('william', 'testPawddassword2', 'fakeid2')
    user3 = getUser('Johnathan', 'test', 'fakeid0_')
    user4 = getUser('robertH', 'test', 'fakeid0_')
    DBA.insertUserInfo(user1)
    DBA.insertUserInfo(user2)
    DBA.insertUserInfo(user3)
    doesUserIdExist = DBA.doesUserIdExist(user4)
    assert doesUserIdExist == True

    del user1
    del user2
    del user3
    del user4
    DBA.clearDatabase()

    user1 = getUser('001', 'teddddstPassword1', 'fakeid1')
    user2 = getUser('02000000009', 'testPawddassword2', 'fakeid2')
    user3 = getUser('joe', 'test', 'fakeid3')
    user4 = getUser('uniqueName', 'password123', 'fakeid4')
    DBA.insertUserInfo(user1)
    DBA.insertUserInfo(user2)
    DBA.insertUserInfo(user3)
    doesUserIdExist = DBA.doesUserIdExist(user4)
    assert doesUserIdExist == False

    del user1
    del user2
    del user3
    del user4
    DBA.clearDatabase()
    DBA.closeConnection()

def test_doesUserExist():
    DBA.createConnection()
    DBA.clearDatabase()

    user1 = getUser('randomename1', 'teddddstPassword1', 'fakeid1')
    user2 = getUser('anotherrand0mName', 'testPawddassword2', 'fakeid2')
    user3 = getUser('09876543', 'test', 'fakeid')
    DBA.insertUserInfo(user1)
    DBA.insertUserInfo(user2)
    DBA.insertUserInfo(user3)
    doesUserExist = DBA.doesUserExist(user3)
    assert doesUserExist == True

    del user1
    del user2
    del user3
    DBA.clearDatabase()

    user1 = getUser('robertH', 'testPassword1', 'fakeid1')
    user2 = getUser('william', 'testPawddassword2', 'fakeid2')
    user3 = getUser('Johnathan@aol.com', 'test', 'fakeid0_')
    user4 = getUser('robertH@aol.com', 'test', 'fakeid0_')
    DBA.insertUserInfo(user1)
    DBA.insertUserInfo(user2)
    DBA.insertUserInfo(user3)
    doesUserExist = DBA.doesUserExist(user4)
    assert doesUserExist == False

    del user1
    del user2
    del user3
    DBA.clearDatabase()

    user1 = getUser('robertH', 'testPassword1', 'fakeid1')
    user2 = getUser('william', 'testPawddassword2', 'fakeid2')
    user3 = getUser('robertH@aol.com', 'test', 'fakeid0__')
    user4 = getUser('robertH@aol.com', 'test', 'fakeid0_')
    DBA.insertUserInfo(user1)
    DBA.insertUserInfo(user2)
    DBA.insertUserInfo(user3)
    doesUserExist = DBA.doesUserExist(user4)
    assert doesUserExist == False

    del user1
    del user2
    del user3
    DBA.clearDatabase()

    user1 = getUser('001', 'teddddstPassword1', 'fakeid1')
    user2 = getUser('02000000009', 'testPawddassword2', 'fakeid2')
    user3 = getUser('joe', 'test', 'fakeid3')
    user4 = getUser('uniqueName', 'password123', 'fakeid4')
    DBA.insertUserInfo(user1)
    DBA.insertUserInfo(user2)
    DBA.insertUserInfo(user3)
    doesUserExist = DBA.doesUserExist(user4)
    assert doesUserExist == False

    del user1
    del user2
    del user3
    DBA.clearDatabase()
    DBA.closeConnection()

def test_handleQueryReturn():
    emptyTuple = ()
    filledTuple1 = (1, 2, 3)
    filledTuple2 = ('bat', 'rat', 'cat')
    assert DBA.handleQueryReturn(emptyTuple) == None
    assert DBA.handleQueryReturn(filledTuple1) == 1
    assert DBA.handleQueryReturn(filledTuple2) == 'bat'
