import pytest
import sys
import os

THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
sys.path.append(THIS_FOLDER + '/../src/DatabaseLayer')
sys.path.append(THIS_FOLDER + '/../src/BusinessLayer/handlers')
sys.path.append(THIS_FOLDER + '/../src/BusinessLayer/models')

from PasswordResetHandler import PasswordResetHandler
from SignUpHandler import SignUpHandler
from LoginHandler import LoginHandler
from DatabaseAccessor import DatabaseAccessor
from User import User

PRH = PasswordResetHandler()
signupHandler = SignUpHandler()
loginHandler = LoginHandler()
DBA = DatabaseAccessor()


def test_handlePasswordReset():
    DBA.createConnection()
    DBA.clearDatabase()

    user = User('test_email@aol.com', 'test_text_password')
    user.hashedPassword = 'test_hashed_password'
    user.setUserId('test_user_id')
    DBA.insertUserInfo(user)

    authToken = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6InRlc3RfZW1haWxAYW9sLmNvbSIsInVzZXIgaWQiOiJ0ZXN0X3VzZXJfaWQifQ.vMQT02nUT0tVfOTolCGSKlSj8cgG6kzhhZ9F6Albq1c'
    passwordResetResponse = PRH.handlePasswordReset(authToken, 'new_test_text_password')
    hashedPassword = DBA.selectHashedPassword(user)
    assert hashedPassword != None
    assert hashedPassword != 'test_hashed_password'
    assert passwordResetResponse == {
        'response string': 'password reset successful',
        'response code': 205
    }

    authToken = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6InRlc3RfZW1haWxAYW9sLmNvbSIsInVzZXIgaWQiOiJ0ZXN0X3VzZXJfaWQifQ.vMQT02nUT0tVfOTolCGSKlSj8cgG6kzhhZ9F6Albq1c'
    passwordResetResponse = PRH.handlePasswordReset(authToken, 'eight___')
    assert passwordResetResponse == {
        'response string': 'password reset successful',
        'response code': 205
    }

    authToken = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6InRlc3RfZW1haWxAYW9sLmNvbSIsInVzZXIgaWQiOiJ0ZXN0X3VzZXJfaWQifQ.vMQT02nUT0tVfOTolCGSKlSj8cgG6kzhhZ9F6Albq1c'
    passwordResetResponse = PRH.handlePasswordReset(authToken, 'sixtyfivechars___________________________________________________')
    assert passwordResetResponse == {
        'response string': 'password reset successful',
        'response code': 205
    }

    # token of wrong user id and right email
    authToken = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6InRlc3RfZW1haWxAYW9sLmNvbSIsInVzZXIgaWQiOiJ0ZXN0X3VzZXJfaWRfIn0.05CM_CQw-uqjhXFserzmNmoHerkqOf4mrYy2Nj1QXNk'
    passwordResetResponse = PRH.handlePasswordReset(authToken, 'new_test_text_password')
    assert passwordResetResponse == {
        'response string': 'password reset unauthorized',
        'response code': 401
    }

    # token of wrong email and right user id
    authToken = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6InRlc3RfZW1haWxfQGFvbC5jb20iLCJ1c2VyIGlkIjoidGVzdF91c2VyX2lkIn0.Hm0xqDmwquuq1qSfE5Od_Mqw_sailF0Vnd5fmx_8bYU'
    passwordResetResponse = PRH.handlePasswordReset(authToken, 'new_test_text_password')
    assert passwordResetResponse == {
        'response string': 'password reset unauthorized',
        'response code': 401
    }

    authToken = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6InRlc3RfZW1haWxAYW9sLmNvbSIsInVzZXIgaWQiOiJ0ZXN0X3VzZXJfaWQifQ.vMQT02nUT0tVfOTolCGSKlSj8cgG6kzhhZ9F6Albq1c'
    passwordResetResponse = PRH.handlePasswordReset(authToken, 'seven__')
    assert passwordResetResponse == {
        'response string': 'password length bad',
        'response code': 402
    }

    authToken = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6InRlc3RfZW1haWxAYW9sLmNvbSIsInVzZXIgaWQiOiJ0ZXN0X3VzZXJfaWQifQ.vMQT02nUT0tVfOTolCGSKlSj8cgG6kzhhZ9F6Albq1c'
    passwordResetResponse = PRH.handlePasswordReset(authToken, 'sixtysixchars_____________________________________________________')
    assert passwordResetResponse == {
        'response string': 'password length bad',
        'response code': 402
    }

    del user
    DBA.clearDatabase()

    # expired token (exp: 1577507364)
    authToken = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6InRlc3RfZW1haWxAYW9sLmNvbSIsInVzZXIgaWQiOiJ0ZXN0X3VzZXJfaWQiLCJleHAiOjE1Nzc1MDczNjR9.i6tja3avfzernS-gVgCyPbIyrFO0g8FMPad_OILDjQ4'
    passwordResetResponse = PRH.handlePasswordReset(authToken, 'new_test_text_password')
    assert passwordResetResponse == {
        'response string': 'password reset unauthorized',
        'response code': 401
    }

    # bad random token
    authToken = 'eyJhbGsciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6InRlc3RfZW1haWxAYW9sLmNvbSIsInVzZXIgaWQiOiJ0ZXN0X3VzZXJfaWQiLCJleHAiOjE1Nzc1MDczNjR9.i6tja3avfzernS-gVgCyPbIyrFO0g8FMPad_OILDjQ4'
    passwordResetResponse = PRH.handlePasswordReset(authToken, 'new_test_text_password')
    assert passwordResetResponse == {
        'response string': 'password reset unauthorized',
        'response code': 401
    }

    # bad random token
    authToken = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6InRlc3RfZW1haWxAYW9sLmNvbSIsInVzZXIgaWQiOiJ0ZXN0X3VzZXJfaWQifQ.dbgrQrWoWOWupUm6x7QVBDm7S7xLrPMCHx6Xz-3ix5k'
    passwordResetResponse = PRH.handlePasswordReset(authToken, 'new_test_text_password')
    assert passwordResetResponse == {
        'response string': 'password reset unauthorized',
        'response code': 401
    }

    # token of non-existent user
    authToken = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6InRlc3RfZW1haWxAYW9sLmNvbSIsInVzZXIgaWQiOiJ0ZXN0X3VzZXJfaWRfIn0.05CM_CQw-uqjhXFserzmNmoHerkqOf4mrYy2Nj1QXNk'
    passwordResetResponse = PRH.handlePasswordReset(authToken, 'new_test_text_password')
    assert passwordResetResponse == {
        'response string': 'password reset unauthorized',
        'response code': 401
    }
