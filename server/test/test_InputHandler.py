import pytest
import sys
sys.path.append('/Users/justinkwan/Documents/WebApps/UserAuthentication/server/src')
from InputHandler import InputHandler
from DatabaseAccessor import DatabaseAccessor

inputHandler     = InputHandler()
databaseAccessor = DatabaseAccessor()

def test_handleUserInput():
    assert inputHandler.handleUserInput('', '') == 'EMPTY_FIELDS'
    assert inputHandler.handleUserInput('', 'password') == 'EMPTY_USERNAME'
    assert inputHandler.handleUserInput('username', '') == 'EMPTY_PASSWORD'
    databaseAccessor.insertUsernamePassword('username', 'password1')
    assert inputHandler.handleUserInput('username', 'randompassword') == 'DUPLICATE_USERNAME'
    databaseAccessor.clearDatabase()
    assert inputHandler.handleUserInput('username', 'password') == 'SUCCESS'
    databaseAccessor.clearDatabase()

def test_checkForExistingUsername():
    databaseAccessor.clearDatabase()

    databaseAccessor.insertUsernamePassword('randomename1', 'teddddstPassword1')
    databaseAccessor.insertUsernamePassword('anotherrand0mName', 'testPawddassword2')
    databaseAccessor.insertUsernamePassword('09876543', 'test')
    databaseAccessor.insertUsernamePassword('johnnotrealperson', 'password123')
    doesUsernameExist = inputHandler.checkForExistingUsername('09876543')

    assert doesUsernameExist == True

    databaseAccessor.clearDatabase()

    databaseAccessor.insertUsernamePassword('robertH', 'teddddstPassword1')
    databaseAccessor.insertUsernamePassword('william', 'testPawddassword2')
    databaseAccessor.insertUsernamePassword('Johnathan', 'test')
    databaseAccessor.insertUsernamePassword('randomguy', 'password123')
    doesUsernameExist = inputHandler.checkForExistingUsername('johnathan')
    assert doesUsernameExist == False

    databaseAccessor.clearDatabase()

    databaseAccessor.insertUsernamePassword('001', 'teddddstPassword1')
    databaseAccessor.insertUsernamePassword('02000000009', 'testPawddassword2')
    databaseAccessor.insertUsernamePassword('joe', 'test')
    databaseAccessor.insertUsernamePassword('testname', 'password123')
    doesUsernameExist = inputHandler.checkForExistingUsername('02000000009')
    assert doesUsernameExist == True

    databaseAccessor.clearDatabase()

def test_checkTextEmpty():
    assert inputHandler.checkTextEmpty('Not Empty') == False
    assert inputHandler.checkTextEmpty('') == True
    assert inputHandler.checkTextEmpty('0987*') == False

def test_handleEmptyFields():
    assert inputHandler.handleEmptyFields('', '') == 'EMPTY_FIELDS'
    assert inputHandler.handleEmptyFields('', 'password') == 'EMPTY_USERNAME'
    assert inputHandler.handleEmptyFields('username', '') == 'EMPTY_PASSWORD'
    assert inputHandler.handleEmptyFields('username', 'password') == 'ALL_FIELDS_FILLED'

def test_parseSelectedField():
    assert inputHandler.parseSelectedField('hello') == 'hello'
    assert inputHandler.parseSelectedField("[(',hello')]") == 'hello'
    assert inputHandler.parseSelectedField('[(,)') == ''
