import pytest
import sys
sys.path.append('/Users/justinkwan/Documents/WebApps/UserAuth/server/src')
from DatabaseAccessor import DatabaseAccessor
from InputHandler import InputHandler

databaseAccessor = DatabaseAccessor()
inputHandler  = InputHandler()

# test username, password and user id inserting function
def test_insertUserInfo():
    databaseAccessor.clearDatabase()

    databaseAccessor.insertUserInfo('testUsername1', 'testPassword1', 'testId1')
    selectedUsername = databaseAccessor.selectUsername('testUsername1')
    selectedPassword = databaseAccessor.selectPassword('testPassword1')
    selectedUserId = databaseAccessor.selectUserId('testId1')
    assert inputHandler.parseSelectedField(selectedUsername) == 'testUsername1'
    assert inputHandler.parseSelectedField(selectedPassword) == 'testPassword1'
    assert inputHandler.parseSelectedField(selectedUserId) == 'testId1'

    databaseAccessor.clearDatabase()

    databaseAccessor.insertUserInfo('09812', '*7%-', 'testId2')
    selectedUsername = databaseAccessor.selectUsername('09812')
    selectedPassword = databaseAccessor.selectPassword('*7%-')
    selectedUserId = databaseAccessor.selectUserId('testId2')
    assert inputHandler.parseSelectedField(selectedUsername) == '09812'
    assert inputHandler.parseSelectedField(selectedPassword) == '*7%-'
    assert inputHandler.parseSelectedField(selectedUserId) == 'testId2'

    databaseAccessor.clearDatabase()

    databaseAccessor.insertUserInfo('-l-&$', '=testpassw0rd', 'testId3')
    selectedUsername = databaseAccessor.selectUsername('-l-&$')
    selectedPassword = databaseAccessor.selectPassword('=testpassw0rd')
    selectedUserId = databaseAccessor.selectUserId('testId3')
    assert inputHandler.parseSelectedField(selectedUsername) == '-l-&$'
    assert inputHandler.parseSelectedField(selectedPassword) == '=testpassw0rd'
    assert inputHandler.parseSelectedField(selectedUserId) == 'testId3'

    databaseAccessor.clearDatabase()

# test username selecting function
def test_selectUsername():
    databaseAccessor.clearDatabase()

    databaseAccessor.insertUserInfo('testUsername1', 'testPassword1', 'testId')
    databaseAccessor.insertUserInfo('testUsername2', 'testPassword2', 'testId')
    databaseAccessor.insertUserInfo('testUsername3', 'testPassword3', 'testId')
    selectedUsername = databaseAccessor.selectUsername('testUsername2')
    parsedSelectedUsername = inputHandler.parseSelectedField(selectedUsername)
    assert parsedSelectedUsername == 'testUsername2'

    databaseAccessor.clearDatabase()

    databaseAccessor.insertUserInfo('fakename', 'teddddstPassword1', 'testId')
    databaseAccessor.insertUserInfo('testdwdadUsername2', 'testPawddassword2', 'testId')
    databaseAccessor.insertUserInfo('w90', 'test', 'testId')
    selectedUsername = databaseAccessor.selectUsername('w90')
    parsedSelectedUsername = inputHandler.parseSelectedField(selectedUsername)
    assert parsedSelectedUsername == 'w90'

    databaseAccessor.clearDatabase()

# test password selecting function
def test_selectPassword():
    databaseAccessor.clearDatabase()

    databaseAccessor.insertUserInfo('rando', 'testPassword1', 'testId')
    databaseAccessor.insertUserInfo('rando2', 'testPassword2', 'testId')
    databaseAccessor.insertUserInfo('rando3', 'testPassword3', 'testId')
    selectedPassword = databaseAccessor.selectPassword('testPassword2')
    parsedSelectedPassword = inputHandler.parseSelectedField(selectedPassword)
    assert parsedSelectedPassword == 'testPassword2'

    databaseAccessor.clearDatabase()

    databaseAccessor.insertUserInfo('name1', 'teddddstPassword1', 'testId')
    databaseAccessor.insertUserInfo('name2', 'testPawddassword2', 'testId')
    databaseAccessor.insertUserInfo('name3', 'test', 'testId')
    selectedPassword = databaseAccessor.selectPassword('nonexistentpassword')
    parsedSelectedPassword = inputHandler.parseSelectedField(selectedPassword)
    assert parsedSelectedPassword == 'None'

    databaseAccessor.clearDatabase()

# test user id selecting function
def test_selectUserId():
    databaseAccessor.clearDatabase()

    databaseAccessor.insertUserInfo('name1', 'teddddstPassword1', 'testId1')
    databaseAccessor.insertUserInfo('name2', 'teddddstPassword2', 'testId2')
    databaseAccessor.insertUserInfo('name3', 'teddddstPassword3', 'testId3')
    selectedUserId = databaseAccessor.selectUserId('testId3')
    assert inputHandler.parseSelectedField(selectedUserId) == 'testId3'

    databaseAccessor.clearDatabase()

    databaseAccessor.insertUserInfo('name1', 'teddddstPassword1', 'testId0')
    databaseAccessor.insertUserInfo('name2', 'teddddstPassword2', 'testId4')
    databaseAccessor.insertUserInfo('name3', 'teddddstPassword3', 'testId9')
    selectedUserId = databaseAccessor.selectUserId('testId4')
    assert inputHandler.parseSelectedField(selectedUserId) == 'testId4'

    databaseAccessor.clearDatabase()
