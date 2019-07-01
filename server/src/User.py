import bcrypt
import uuid

class User():

    def __init__(self, username, textPassword):
        self.username       = username
        self.textPassword   = textPassword
        self.hashedPassword = ''
        self.userId         = str(uuid.uuid4())

    def getUsername(self):
        return self.username

    def getTextPassword(self):
        return self.textPassword

    def getHashedPassword(self):
        return self.hashedPassword

    def getUserId(self):
        return self.userId

    def encryptAndUpdatePassword(self, password):
        hashedPassword = bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt())
        self.hashedPassword = str(hashedPassword)

    # bcrypt.check_password_hash(pw_hash, 'testpassword') # returns True
