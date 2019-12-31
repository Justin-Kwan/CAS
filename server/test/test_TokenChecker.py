import pytest
import sys
import os
import jwt

THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
sys.path.append(THIS_FOLDER + '/../src/BusinessLayer')

from TokenChecker import TokenChecker


tokenChecker = TokenChecker()

def test_getTokenPayload():
    userId = tokenChecker.getTokenPayload('eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJlbWFpbCI6InJhbmRvbXVzZXIxQGdtYWlsLmNvbSIsInVzZXIgaWQiOiJmZjQ0MDZmYy02N2IyLTRmODYtYjJkZC00ZjliMzVjNjQyMDIifQ.vQHMuzxyUF7E3V_liaWj3xmy8IptoI-mQYV-HFKilLw')
    assert userId == {
        "email": "randomuser1@gmail.com",
        "user id": "ff4406fc-67b2-4f86-b2dd-4f9b35c64202",
    }

    userId = tokenChecker.getTokenPayload('eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJlbWFpbCI6InJhbmRvbXVzZXIyQGdtYWlsLmNvbSIsInVzZXIgaWQiOiJnZzQ0MDZmYy02N2IyLTRmODYtYjJkZC00ZjliMzVjNjQzMDEifQ.YSLio5MxY8layIdStVbbvD7hLu6tUbJb1dvo00Urfac')
    assert userId == {
        "email": "randomuser2@gmail.com",
        "user id": "gg4406fc-67b2-4f86-b2dd-4f9b35c64301",
    }

    userId = tokenChecker.getTokenPayload('eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6InVzZXIxMDkiLCJ1c2VyIGlkIjoiZThlMTZiNmYtY2Q4MS00MTM2LTlkNTQtNGMyOTI0NjljNWVlIn0.2Um9i0cguCyoaf3Wrx3OTUY_NmSzol7Q4KXcqWsfZXU')
    assert userId == False

    # expired token (exp: 1577507364)
    userId = tokenChecker.getTokenPayload('eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJlbWFpbCI6Indvd0BkLmNhIiwidXNlciBpZCI6IjFiOTQ3NGU2LTlmMjItNDg0ZS1iNWZmLTI1YzY2ODEzNjQzYSIsImV4cCI6MTU3NzUwNzM2NH0.TUdciTxZ0wio5Hk-spxL4rrR4r6fghTlZ09w4_oR8Qk')
    assert userId == False

    userId = tokenChecker.getTokenPayload('e')
    assert userId == False

    userId = tokenChecker.getTokenPayload('')
    assert userId == False

    userId = tokenChecker.getTokenPayload(' ')
    assert userId == False

    userId = tokenChecker.getTokenPayload(None)
    assert userId == False

    userId = tokenChecker.getTokenPayload(123)
    assert userId == False

def test_loadSecretKeyFromFile():
    tokenChecker.loadSecretKeyFromFile()
    assert tokenChecker.SECRET_KEY == 'fake_secret_key'
