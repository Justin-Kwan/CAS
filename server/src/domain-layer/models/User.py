import bcrypt
import uuid
import jwt
import datetime

class User():

    def __init__(self, email, textPassword):
        self.email          = email
        self.textPassword   = textPassword
        self.hashedPassword = None
        self.userId         = None
        self.authToken      = None

    def getEmail(self):
        return self.email

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

    def setAuthToken(self, authToken):
        self.authToken = authToken

    def encryptAndSetPassword(self):
        hashedPassword = bcrypt.hashpw(self.textPassword.encode('utf-8'), bcrypt.gensalt())
        # generated password is encoded so must decode before storing in db
        self.hashedPassword = hashedPassword.decode()

    def generateAndSetUserId(self):
        self.userId = str(uuid.uuid4())

    def generateAndSetAuthToken(self):
        email = self.getEmail()
        userId = self.getUserId()
        tokenExpiryTime = datetime.datetime.utcnow() + datetime.timedelta(hours=3)

        authTokenPayload = {
            'email': email,
            'user id': userId,
            'exp': tokenExpiryTime
        }

        self.authToken = jwt.encode(authTokenPayload, 'fake_secret_key', algorithm='HS256').decode()
