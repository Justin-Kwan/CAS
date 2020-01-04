import os
import jwt
import json

class TokenChecker:

    def __init__(self):
        self.THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
        self.SECRET_KEY_LOCATION = os.path.join(self.THIS_FOLDER, '../../resources/token-secret-key.json')
        self.SECRET_KEY = None
        self.BAD_TOKEN = False

    def getTokenPayload(self, authToken):
        self.loadSecretKeyFromFile()
        try:
            tokenPayload = jwt.decode(authToken, self.SECRET_KEY, algorithms=['HS256'])
            return tokenPayload
        except jwt.InvalidTokenError:
            return self.BAD_TOKEN

    def loadSecretKeyFromFile(self):
        with open(self.SECRET_KEY_LOCATION, 'r') as myfile:
            data = myfile.read()
            contents = json.loads(data)
            self.SECRET_KEY = contents['auth-token-secret-key']
