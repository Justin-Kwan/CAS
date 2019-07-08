import pytest
import sys
sys.path.append('/Users/justinkwan/Documents/WebApps/UserAuth/server/src/BusinessLayer/handlers')
sys.path.append('/Users/justinkwan/Documents/WebApps/UserAuth/server/src/BusinessLayer/models')
sys.path.append('/Users/justinkwan/Documents/WebApps/UserAuth/server/src/BusinessLayer')
sys.path.append('/Users/justinkwan/Documents/WebApps/UserAuth/server/src/DatabaseLayer')
from DatabaseAccessor import DatabaseAccessor
from InputValidator   import InputValidator
from User             import User

DBA = DatabaseAccessor()
inputValidator = InputValidator()

def getUser(username, password, userId):
    user = User(username, password)
    user.encryptAndUpdatePassword(password)
    user.updateUserId(userId)
    return user

# test username, password and user id inserting function
def test_insertUserInfo():
    DBA.clearDatabase()

    user = getUser('testUsername1', 'testPassword1', 'testId1')
    DBA.insertUserInfo(user)
    selectedUsername = DBA.selectUsername(user)
    selectedHashedPassword = DBA.selectHashedPassword(user)
    selectedUserId = DBA.selectUserId(user)
    assert selectedUsername == 'testUsername1'
    assert selectedHashedPassword != None
    assert selectedUserId == 'testId1'

    del user
    DBA.clearDatabase()

    user = getUser('09812', '*7%-', 'testId2')
    DBA.insertUserInfo(user)
    selectedUsername = DBA.selectUsername(user)
    selectedHashedPassword = DBA.selectHashedPassword(user)
    selectedUserId = DBA.selectUserId(user)
    assert selectedUsername == '09812'
    assert selectedHashedPassword != None
    assert selectedUserId == 'testId2'

    del user
    DBA.clearDatabase()

    user = getUser('-l-&$', '=testpassw0rd', 'testId3')
    DBA.insertUserInfo(user)
    selectedUsername = DBA.selectUsername(user)
    selectedHashedPassword = DBA.selectHashedPassword(user)
    selectedUserId = DBA.selectUserId(user)
    assert selectedUsername == '-l-&$'
    assert selectedHashedPassword != None
    assert selectedUserId == 'testId3'

    del user
    DBA.clearDatabase()

    user = getUser('fake-user', 'password123', '')
    user.generateAndUpdateUserId()
    DBA.insertUserInfo(user)
    selectedUsername = DBA.selectUsername(user)
    selectedHashedPassword = DBA.selectHashedPassword(user)
    selectedUserId = DBA.selectUserId(user)
    assert selectedUsername == 'fake-user'
    assert selectedHashedPassword != None
    assert selectedUserId == user.getUserId()

    del user
    DBA.clearDatabase()

# test username selecting function
def test_selectUsername():
    DBA.clearDatabase()

    user1 = getUser('testUsername1', 'testPassword1', 'testId')
    user2 = getUser('testUsername2', 'testPassword2', 'testId')
    user3 = getUser('testUsername3', 'testPassword3', 'testId')
    DBA.insertUserInfo(user1)
    DBA.insertUserInfo(user2)
    DBA.insertUserInfo(user3)
    selectedUsername = DBA.selectUsername(user2)
    assert selectedUsername == 'testUsername2'

    del user1
    del user2
    del user3
    DBA.clearDatabase()

    user1 = getUser('fakename', 'teddddstPassword1', 'testId')
    user2 = getUser('testdwdadUsername2', 'testPawddassword2', 'testId')
    user3 = getUser('w90', 'test', 'testId')
    DBA.insertUserInfo(user1)
    DBA.insertUserInfo(user2)
    DBA.insertUserInfo(user3)
    selectedUsername = DBA.selectUsername(user3)
    assert selectedUsername == 'w90'

    del user1
    del user2
    del user3
    DBA.clearDatabase()

# test password selecting function
def test_selectHashedPassword():
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

# test user id selecting function
def test_selectUserId():
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

def test_checkForExistingUsername():
    DBA.clearDatabase()

    user1 = getUser('randomename1', 'teddddstPassword1', 'fakeid1')
    user2 = getUser('anotherrand0mName', 'testPawddassword2', 'fakeid2')
    user3 = getUser('09876543', 'test', 'fakeid3')
    user4 = getUser('09876543', 'test', 'fakeid4')
    DBA.insertUserInfo(user1)
    DBA.insertUserInfo(user2)
    DBA.insertUserInfo(user3)
    doesUsernameExist = DBA.checkForExistingUsername(user4)
    assert doesUsernameExist == True

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
    doesUsernameExist = DBA.checkForExistingUsername(user4)
    assert doesUsernameExist == True

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
    doesUsernameExist = DBA.checkForExistingUsername(user4)
    assert doesUsernameExist == False

    del user1
    del user2
    del user3
    del user4
    DBA.clearDatabase()


def test_handleQueryReturn():
    emptyTuple = ()
    filledTuple1 = (1, 2, 3)
    filledTuple2 = ('bat', 'rat', 'cat')
    assert DBA.handleQueryReturn(emptyTuple) == None
    assert DBA.handleQueryReturn(filledTuple1) == 1
    assert DBA.handleQueryReturn(filledTuple2) == 'bat'
