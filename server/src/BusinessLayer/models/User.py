import bcrypt
import uuid
import jwt
import datetime

class User():

    def __init__(self, username, textPassword):
        self.username       = username
        self.textPassword   = textPassword
        self.hashedPassword = None
        self.userId         = None
        self.securityToken  = None

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

    def updateUserId(self, userId):
        self.userId = userId

    def encryptAndUpdatePassword(self, password):
        hashedPassword = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        # generated password is encoded so must decode before storing in db
        self.hashedPassword = hashedPassword.decode()

    def generateAndUpdateUserId(self):
        self.userId = str(uuid.uuid4())

    def generateAndUpdateSecurityToken(self):
        username = self.getUsername()
        userId = self.getUserId()
        tokenExpiryTime = datetime.datetime.utcnow() + datetime.timedelta(hours=24)
        self.securityToken = jwt.encode({'username': username, 'user id': userId, 'exp': tokenExpiryTime}, 'fake_secret_key', algorithm='HS256').decode()
