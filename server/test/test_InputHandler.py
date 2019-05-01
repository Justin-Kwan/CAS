import pytest
import sys
sys.path.append('/Users/justinkwan/Documents/WebApps/UserAuth/server/src')
from InputHandler import InputHandler
from DatabaseAccessor import DatabaseAccessor

inputHandler     = InputHandler()
databaseAccessor = DatabaseAccessor()

def test_handleUserInput():
    assert inputHandler.handleUserInput('', '') == 'EMPTY_FIELDS'
    assert inputHandler.handleUserInput('', 'password') == 'EMPTY_USERNAME'
    assert inputHandler.handleUserInput('username', '') == 'EMPTY_PASSWORD'
    databaseAccessor.insertUsernamePassword('username', 'password1')
    assert inputHandler.handleUserInput('username', 'password1') == 'DUPLICATE_USERNAME'
    databaseAccessor.clearDatabase()
    assert inputHandler.handleUserInput('username', 'password') == 'SUCCESS'
    databaseAccessor.clearDatabase()
    assert inputHandler.handleUserInput('usern>ame', 'password') == 'INVALID_USERNAME_CHARS'
    databaseAccessor.clearDatabase()
    assert inputHandler.handleUserInput('-username', 'password') == 'INVALID_USERNAME_CHARS'
    databaseAccessor.clearDatabase()
    assert inputHandler.handleUserInput('username;', 'password') == 'INVALID_USERNAME_CHARS'
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
