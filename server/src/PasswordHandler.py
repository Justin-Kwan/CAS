import bcrypt

class PasswordHandler():

    def encryptPassword(self, password):
        hashedPassword = bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt())
        return str(hashedPassword)

    # bcrypt.check_password_hash(pw_hash, 'hunter2') # returns True
