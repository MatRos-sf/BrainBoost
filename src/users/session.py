import base64

import bcrypt


def hash_password(password: str):
    """The methods hash provided password and return hash password as a string"""
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode(), salt)
    # convert to string
    return base64.b64encode(hashed_password).decode()


def verify_password(stored_hash: str, password: str):
    """Checks that provided password matches with the stored password"""
    stored_hash_bytes = base64.b64decode(stored_hash)
    return bcrypt.checkpw(password.encode(), stored_hash_bytes)


class UserSession:
    def __init__(self, username, password_hash):
        self.username = username
        self._password = password_hash
        self.stats = None
