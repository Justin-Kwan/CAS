import pytest
import sys
sys.path.append('/Users/justinkwan/Documents/WebApps/UserAuthentication/server/src')
from UsernameHandler import UsernameHandler
from DatabaseAccessor import DatabaseAccessor

usernameHandler  = UsernameHandler()
databaseAccessor = DatabaseAccessor()

def test_checkForInvalidUsernameChars():
    assert usernameHandler.checkForInvalidUsernameChars("string2") == True
    assert usernameHandler.checkForInvalidUsernameChars("fake$username)") == False
    assert usernameHandler.checkForInvalidUsernameChars(")(*&^)") == False
    assert usernameHandler.checkForInvalidUsernameChars(")(*&^)textTest*&^%moretestis*fun';:") == False

def test_parseSelectedField():
    assert usernameHandler.parseSelectedField('hello') == 'hello'
    assert usernameHandler.parseSelectedField("[(',hello')]") == 'hello'
    assert usernameHandler.parseSelectedField('[(,)') == ''

def test_checkForExistingUsername():
    databaseAccessor.clearDatabase()

    databaseAccessor.insertUsernamePassword('randomename1', 'teddddstPassword1')
    databaseAccessor.insertUsernamePassword('anotherrand0mName', 'testPawddassword2')
    databaseAccessor.insertUsernamePassword('09876543', 'test')
    databaseAccessor.insertUsernamePassword('johnnotrealperson', 'password123')
    doesUsernameExist = usernameHandler.checkForExistingUsername('09876543')
    assert doesUsernameExist == True

    databaseAccessor.clearDatabase()

    databaseAccessor.insertUsernamePassword('robertH', 'teddddstPassword1')
    databaseAccessor.insertUsernamePassword('william', 'testPawddassword2')
    databaseAccessor.insertUsernamePassword('Johnathan', 'test')
    databaseAccessor.insertUsernamePassword('randomguy', 'password123')
    doesUsernameExist = usernameHandler.checkForExistingUsername('johnathan')
    assert doesUsernameExist == False

    databaseAccessor.clearDatabase()

    databaseAccessor.insertUsernamePassword('001', 'teddddstPassword1')
    databaseAccessor.insertUsernamePassword('02000000009', 'testPawddassword2')
    databaseAccessor.insertUsernamePassword('joe', 'test')
    databaseAccessor.insertUsernamePassword('testname', 'password123')
    doesUsernameExist = usernameHandler.checkForExistingUsername('02000000009')
    assert doesUsernameExist == True

    databaseAccessor.clearDatabase()
