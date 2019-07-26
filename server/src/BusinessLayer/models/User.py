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
        self.authToken      = None

    def getUsername(self):
        return self.username

    def getTextPassword(self):
        return self.textPassword

    def getHashedPassword(self):
        return self.hashedPassword

    def getUserId(self):
        return self.userId

    def getAuthToken(self):
        return self.authToken

    def setUserId(self, userId):
        self.userId = userId

    def encryptAndSetPassword(self, password):
        hashedPassword = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        # generated password is encoded so must decode before storing in db
        self.hashedPassword = hashedPassword.decode()

    def generateAndSetUserId(self):
        self.userId = str(uuid.uuid4())

    def generateAndSetAuthToken(self):
        username = self.getUsername()
        userId = self.getUserId()
        tokenExpiryTime = datetime.datetime.utcnow() + datetime.timedelta(hours=3)

        authTokenPayload = {
            'username': username,
            'user id': userId,
            'exp': tokenExpiryTime
        }

        self.authToken = jwt.encode(authTokenPayload, 'fake_secret_key', algorithm='HS256').decode()
