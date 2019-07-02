import bcrypt
import uuid
import jwt
import datetime

class User():

    def __init__(self, username, textPassword):
        self.username       = username
        self.textPassword   = textPassword
        self.hashedPassword = ''
        self.userId         = str(uuid.uuid4())
        self.securityToken  = ''

    def getUsername(self):
        return self.username

    def getTextPassword(self):
        return self.textPassword

    def getHashedPassword(self):
        return self.hashedPassword

    def getUserId(self):
        return self.userId

    def getSecurityToken(self):
        return self.securityToken

    # update User Id!

    

    def encryptAndUpdatePassword(self, password):
        hashedPassword = bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt())
        self.hashedPassword = str(hashedPassword)

    # generate and update user id!

    def generateAndUpdateSecurityToken(self):
        username = self.getUsername()
        userId = self.getUserId()
        tokenExpiryTime = datetime.datetime.utcnow() + datetime.timedelta(hours=24)
        self.securityToken = jwt.encode({'username': username, 'user id': userId, 'exp': tokenExpiryTime}, 'fake_secret_key', algorithm='HS256')
