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
    inputHandler.handleUserInput('Username', 'password')
    assert inputHandler.handleUserInput('username', 'password') == 'DUPLICATE_USERNAME'
    databaseAccessor.clearDatabase()
    inputHandler.handleUserInput('username', 'password')
    assert inputHandler.handleUserInput('Username', 'password') == 'DUPLICATE_USERNAME'
    databaseAccessor.clearDatabase()
    inputHandler.handleUserInput('UsErNAME', 'password')
    assert inputHandler.handleUserInput('USERNAME', 'password') == 'DUPLICATE_USERNAME'
    databaseAccessor.clearDatabase()
    inputHandler.handleUserInput('USERNAME', 'password')
    assert inputHandler.handleUserInput('username', 'password') == 'DUPLICATE_USERNAME'
    databaseAccessor.clearDatabase()

def test_checkTextEmpty():
    assert inputHandler.checkTextEmpty('Not Empty') == False
    assert inputHandler.checkTextEmpty('') == True
    assert inputHandler.checkTextEmpty('0987*') == False

'''
    Testing username and password length constraints for input validation
'''
def test_checkInputLength():
    # middle case
    assert inputHandler.checkInputLength('USERNAME', 'testusername') == True
    # edge case
    assert inputHandler.checkInputLength('USERNAME', 'usrnmm') == True
    assert inputHandler.checkInputLength('USERNAME', 'testusernametestusernametestusernam') == True
    assert inputHandler.checkInputLength('USERNAME', 'testusernametestusernametestusername') == False
    assert inputHandler.checkInputLength('USERNAME', 'usrnm') == False
    assert inputHandler.checkInputLength('USERNAME', '') == False
    assert inputHandler.checkInputLength('USERNAME', 'testusernametestusernametestusernametestusernametestusernametestusername') == False

def test_handleEmptyFields():
    assert inputHandler.handleEmptyFields('', '') == 'EMPTY_FIELDS'
    assert inputHandler.handleEmptyFields('', 'password') == 'EMPTY_USERNAME'
    assert inputHandler.handleEmptyFields('username', '') == 'EMPTY_PASSWORD'
    assert inputHandler.handleEmptyFields('username', 'password') == 'ALL_FIELDS_FILLED'
