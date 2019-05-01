import pytest
import sys
sys.path.append('/Users/justinkwan/Documents/WebApps/UserAuth/server/src')
from DatabaseAccessor import DatabaseAccessor
from UsernameHandler import UsernameHandler

databaseAccessor = DatabaseAccessor()
usernameHandler  = UsernameHandler()

def test_insertUsernamePassword():
    databaseAccessor.clearDatabase()

    databaseAccessor.insertUsernamePassword('testUsername1', 'testPassword1')
    selectedUsername = databaseAccessor.selectUsername('testUsername1')
    selectedPassword = databaseAccessor.selectPassword('testPassword1')
    assert usernameHandler.parseSelectedField(selectedUsername) == 'testUsername1'
    assert usernameHandler.parseSelectedField(selectedPassword) == 'testPassword1'

    databaseAccessor.clearDatabase()

    databaseAccessor.insertUsernamePassword('09812', '*7%-')
    selectedUsername = databaseAccessor.selectUsername('09812')
    selectedPassword = databaseAccessor.selectPassword('*7%-')
    assert usernameHandler.parseSelectedField(selectedUsername) == '09812'
    assert usernameHandler.parseSelectedField(selectedPassword) == '*7%-'

    databaseAccessor.clearDatabase()

    databaseAccessor.insertUsernamePassword('-l-&$', '=testpassw0rd')
    selectedUsername = databaseAccessor.selectUsername('-l-&$')
    selectedPassword = databaseAccessor.selectPassword('=testpassw0rd')
    assert usernameHandler.parseSelectedField(selectedUsername) == '-l-&$'
    assert usernameHandler.parseSelectedField(selectedPassword) == '=testpassw0rd'

    databaseAccessor.clearDatabase()

def test_selectUsername():
    databaseAccessor.clearDatabase()

    databaseAccessor.insertUsernamePassword('testUsername1', 'testPassword1')
    databaseAccessor.insertUsernamePassword('testUsername2', 'testPassword2')
    databaseAccessor.insertUsernamePassword('testUsername3', 'testPassword3')
    selectedUsername = databaseAccessor.selectUsername('testUsername2')
    parsedSelectedUsername = usernameHandler.parseSelectedField(selectedUsername)
    assert parsedSelectedUsername == 'testUsername2'

    databaseAccessor.clearDatabase()

    databaseAccessor.insertUsernamePassword('fakename', 'teddddstPassword1')
    databaseAccessor.insertUsernamePassword('testdwdadUsername2', 'testPawddassword2')
    databaseAccessor.insertUsernamePassword('w90', 'test')
    selectedUsername = databaseAccessor.selectUsername('w90')
    parsedSelectedUsername = usernameHandler.parseSelectedField(selectedUsername)
    assert parsedSelectedUsername == 'w90'

    databaseAccessor.clearDatabase()

def test_selectUsername():
    databaseAccessor.clearDatabase()

    databaseAccessor.insertUsernamePassword('testUsername1', 'testPassword1')
    databaseAccessor.insertUsernamePassword('testUsername2', 'testPassword2')
    databaseAccessor.insertUsernamePassword('testUsername3', 'testPassword3')
    selectedUsername = databaseAccessor.selectUsername('testUsername2')
    parsedSelectedUsername = usernameHandler.parseSelectedField(selectedUsername)
    assert parsedSelectedUsername == 'testUsername2'

    databaseAccessor.clearDatabase()

    databaseAccessor.insertUsernamePassword('fakename', 'teddddstPassword1')
    databaseAccessor.insertUsernamePassword('testdwdadUsername2', 'testPawddassword2')
    databaseAccessor.insertUsernamePassword('w90', 'test')
    selectedUsername = databaseAccessor.selectUsername('w90')
    parsedSelectedUsername = usernameHandler.parseSelectedField(selectedUsername)
    assert parsedSelectedUsername == 'w90'

    databaseAccessor.clearDatabase()

def test_selectPassword():
    databaseAccessor.clearDatabase()

    databaseAccessor.insertUsernamePassword('rando', 'testPassword1')
    databaseAccessor.insertUsernamePassword('rando2', 'testPassword2')
    databaseAccessor.insertUsernamePassword('rando3', 'testPassword3')
    selectedPassword = databaseAccessor.selectPassword('testPassword2')
    parsedSelectedPassword = usernameHandler.parseSelectedField(selectedPassword)
    assert parsedSelectedPassword == 'testPassword2'

    databaseAccessor.clearDatabase()

    databaseAccessor.insertUsernamePassword('name1', 'teddddstPassword1')
    databaseAccessor.insertUsernamePassword('name2', 'testPawddassword2')
    databaseAccessor.insertUsernamePassword('name3', 'test')
    selectedPassword = databaseAccessor.selectPassword('nonexistentpassword')
    parsedSelectedPassword = usernameHandler.parseSelectedField(selectedPassword)
    assert parsedSelectedPassword == 'None'

    databaseAccessor.clearDatabase()
