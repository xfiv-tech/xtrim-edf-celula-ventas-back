from flask_bcrypt import Bcrypt


bcrypt = Bcrypt()


def encryptPassword(password):
    return bcrypt.generate_password_hash(password).decode('utf-8')


def checkPassword(password, passwordHash):
    return bcrypt.check_password_hash(passwordHash, password)
 