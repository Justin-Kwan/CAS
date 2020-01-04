import pytest
import sys
import os

THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
sys.path.append(THIS_FOLDER + '/../src/domain-layer/handlers')
sys.path.append(THIS_FOLDER + '/../src/domain-layer/models')
sys.path.append(THIS_FOLDER + '/../src/database-layer')

from User import User
from DatabaseAccessor import DatabaseAccessor
from TokenCheckHandler import TokenCheckHandler

tokenCheckHandler = TokenCheckHandler()
DBA = DatabaseAccessor()

def getUser(email, userId, password):
    user = User(email, password)
    user.userId = userId
    user.hashedPassword = "hashed_password"
    return user

def test_handleTokenCheck():

    user = getUser("randomuser1@gmail.com", 'ff4406fc-67b2-4f86-b2dd-4f9b35c64202', "a_good_password_123")
    DBA.createConnection()
    DBA.insertUserInfo(user)
    DBA.closeConnection()

    jsonResponse = tokenCheckHandler.handleTokenCheck('eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJlbWFpbCI6InJhbmRvbXVzZXIxQGdtYWlsLmNvbSIsInVzZXIgaWQiOiJmZjQ0MDZmYy02N2IyLTRmODYtYjJkZC00ZjliMzVjNjQyMDIifQ.vQHMuzxyUF7E3V_liaWj3xmy8IptoI-mQYV-HFKilLw')
    assert jsonResponse == {
        'is user authorized': True,
        'user id': 'ff4406fc-67b2-4f86-b2dd-4f9b35c64202',
        'response code': 200
    }

    user = getUser("randomuser2@gmail.com", 'gg4406fc-67b2-4f86-b2dd-4f9b35c64301', "a_good_password_123")
    DBA.createConnection()
    DBA.insertUserInfo(user)
    DBA.closeConnection()

    jsonResponse = tokenCheckHandler.handleTokenCheck('eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJlbWFpbCI6InJhbmRvbXVzZXIyQGdtYWlsLmNvbSIsInVzZXIgaWQiOiJnZzQ0MDZmYy02N2IyLTRmODYtYjJkZC00ZjliMzVjNjQzMDEifQ.YSLio5MxY8layIdStVbbvD7hLu6tUbJb1dvo00Urfac')
    assert jsonResponse == {
        'is user authorized': True,
        'user id': 'gg4406fc-67b2-4f86-b2dd-4f9b35c64301',
        'response code': 200
    }

    # bad random token
    jsonResponse = tokenCheckHandler.handleTokenCheck('eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJlbWFpbCI6InJhbmRvbXVzZXIyQGdtYWlsLmNvbSIsInVzZXIgaWQiOiJnZzQ0MDZmYy02N2IyLTRmODYtYjJkZC00ZjliMzVjNjQzMDEifQ.YSLdio5MxY8layIdStVbbvD7hLu6tUbJb1dvo00Urfac')
    assert jsonResponse == {
        'is user authorized': False,
        'user id': 'unauthorized',
        'response code': 401
    }

    # bad random token
    jsonResponse = tokenCheckHandler.handleTokenCheck('eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJlbWFpbCI6Indvd0BkLmNhIiwidXNlciBpZCI6IjFiOTQ3NGU2LTlmMjItNDg0ZS1iNWZmLTI1YzY2ODEzNjQzYSIsImV4cCI6MTU3NzUwNzM2NH0.VFFH7e7mel095Y9zpruv7FSjg-gewrp1fIeSorAxjG4')
    assert jsonResponse == {
        'is user authorized': False,
        'user id': 'unauthorized',
        'response code': 401
    }

    # bad random token
    jsonResponse = tokenCheckHandler.handleTokenCheck('eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c')
    assert jsonResponse == {
        'is user authorized': False,
        'user id': 'unauthorized',
        'response code': 401
    }

    # expired token (exp: 1577507364)
    jsonResponse = tokenCheckHandler.handleTokenCheck('eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJlbWFpbCI6Indvd0BkLmNhIiwidXNlciBpZCI6IjFiOTQ3NGU2LTlmMjItNDg0ZS1iNWZmLTI1YzY2ODEzNjQzYSIsImV4cCI6MTU3NzUwNzM2NH0.TUdciTxZ0wio5Hk-spxL4rrR4r6fghTlZ09w4_oR8Qk')
    assert jsonResponse == {
        'is user authorized': False,
        'user id': 'unauthorized',
        'response code': 401
    }
