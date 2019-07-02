import pytest
import sys
sys.path.append('/Users/justinkwan/Documents/WebApps/UserAuth/server/src')
from DatabaseAccessor import DatabaseAccessor
from InputHandler import InputHandler

DBA = DatabaseAccessor()
inputHandler  = InputHandler()

# test username, password and user id inserting function
def test_insertUserInfo():
    DBA.clearDatabase()

    DBA.insertUserInfo('testUsername1', 'testPassword1', 'testId1')
    selectedUsername = DBA.selectUsername('testUsername1')
    selectedHashedPassword = DBA.selectHashedPassword('testUsername1')
    selectedUserId = DBA.selectUserId('testId1')
    assert selectedUsername == 'testUsername1'
    assert selectedHashedPassword == 'testPassword1'
    assert selectedUserId == 'testId1'

    DBA.clearDatabase()

    DBA.insertUserInfo('09812', '*7%-', 'testId2')
    selectedUsername = DBA.selectUsername('09812')
    selectedHashedPassword = DBA.selectHashedPassword('09812')
    selectedUserId = DBA.selectUserId('testId2')
    assert selectedUsername == '09812'
    assert selectedHashedPassword == '*7%-'
    assert selectedUserId == 'testId2'

    DBA.clearDatabase()

    DBA.insertUserInfo('-l-&$', '=testpassw0rd', 'testId3')
    selectedUsername = DBA.selectUsername('-l-&$')
    selectedHashedPassword = DBA.selectHashedPassword('-l-&$')
    selectedUserId = DBA.selectUserId('testId3')
    assert selectedUsername == '-l-&$'
    assert selectedHashedPassword == '=testpassw0rd'
    assert selectedUserId == 'testId3'

    DBA.clearDatabase()

    DBA.insertUserInfo('-l-&$', '=testpassw0rd', 'testId3')
    selectedUsername = DBA.selectUsername('-l--&$')
    selectedHashedPassword = DBA.selectHashedPassword('-l--&$')
    selectedUserId = DBA.selectUserId('testId30')
    assert selectedUsername == None
    assert selectedHashedPassword == None
    assert selectedUserId == None

    DBA.clearDatabase()

# test username selecting function
def test_selectUsername():
    DBA.clearDatabase()

    DBA.insertUserInfo('testUsername1', 'testPassword1', 'testId')
    DBA.insertUserInfo('testUsername2', 'testPassword2', 'testId')
    DBA.insertUserInfo('testUsername3', 'testPassword3', 'testId')
    selectedUsername = DBA.selectUsername('testUsername2')
    assert selectedUsername == 'testUsername2'

    DBA.clearDatabase()

    DBA.insertUserInfo('fakename', 'teddddstPassword1', 'testId')
    DBA.insertUserInfo('testdwdadUsername2', 'testPawddassword2', 'testId')
    DBA.insertUserInfo('w90', 'test', 'testId')
    selectedUsername = DBA.selectUsername('w90')
    assert selectedUsername == 'w90'

    DBA.clearDatabase()

    DBA.insertUserInfo('fakename3', 'teddddstPassword1', 'testId')
    DBA.insertUserInfo('testdwdadUsername3', 'testPawddassword2', 'testId')
    DBA.insertUserInfo('3', 'test', 'testId')
    selectedUsername = DBA.selectUsername('35')
    assert selectedUsername == None

    DBA.clearDatabase()

# test password selecting function
def test_selectHashedPassword():
    DBA.clearDatabase()

    DBA.insertUserInfo('rando', 'testPassword1', 'testId')
    DBA.insertUserInfo('rando2', 'testPassword2', 'testId')
    DBA.insertUserInfo('rando3', 'testPassword3', 'testId')
    selectedHashedPassword = DBA.selectHashedPassword('rando2')
    assert selectedHashedPassword == 'testPassword2'

    DBA.clearDatabase()

    DBA.insertUserInfo('name1', 'teddddstPassword1', 'testId')
    DBA.insertUserInfo('name2', 'testPawddassword2', 'testId')
    DBA.insertUserInfo('name3', 'test', 'testId')
    selectedHashedPassword = DBA.selectHashedPassword('name4')
    assert selectedHashedPassword == None

    DBA.clearDatabase()

# test user id selecting function
def test_selectUserId():
    DBA.clearDatabase()

    DBA.insertUserInfo('name1', 'teddddstPassword1', 'testId1')
    DBA.insertUserInfo('name2', 'teddddstPassword2', 'testId2')
    DBA.insertUserInfo('name3', 'teddddstPassword3', 'testId3')
    selectedUserId = DBA.selectUserId('testId3')
    assert selectedUserId == 'testId3'

    DBA.clearDatabase()

    DBA.insertUserInfo('name1', 'teddddstPassword1', 'testId0')
    DBA.insertUserInfo('name2', 'teddddstPassword2', 'testId4')
    DBA.insertUserInfo('name3', 'teddddstPassword3', 'testId9')
    selectedUserId = DBA.selectUserId('testId4')
    assert selectedUserId == 'testId4'

    DBA.clearDatabase()

    DBA.insertUserInfo('name1', 'teddddstPassword1', 'testId0')
    DBA.insertUserInfo('name2', 'teddddstPassword2', 'testId4')
    DBA.insertUserInfo('name3', 'teddddstPassword3', 'testId9')
    selectedUserId = DBA.selectUserId('testId5')
    assert selectedUserId == None

    DBA.clearDatabase()

def test_handleQueryReturn():
    emptyTuple = ()
    filledTuple1 = (1, 2, 3)
    filledTuple2 = ('bat', 'rat', 'cat')
    assert DBA.handleQueryReturn(emptyTuple) == None
    assert DBA.handleQueryReturn(filledTuple1) == 1
    assert DBA.handleQueryReturn(filledTuple2) == 'bat'
