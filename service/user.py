import base64
import hmac

from constants import PWD_HASH_SOLT, PWD_HASH_ITERATIONS
from dao.user import UserDAO
import hashlib

class UserService:

    def __init__(self, dao: UserDAO):
        self.dao = dao

    def get_all(self):
        return self.dao.get_all()

    def get_one(self, uid):
        return self.dao.get_one(uid)

    def get_by_username(self, username):
        return self.dao.get_by_username(username)

    def create(self, data_user):
        data_user['password'] = self.make_password(data_user.get('password'))
        return self.dao.create(data_user)

    def update(self, data_user):
        data_user['password'] = self.make_password(data_user.get('password'))

        return self.dao.update(data_user)

    def delete(self, uid):
        return self.dao.delete(uid)

    def make_password(self, password):
        pass_hash = hashlib.pbkdf2_hmac('sha256',
                                         password.encode('utf-8'),
                                         PWD_HASH_SOLT,
                                         PWD_HASH_ITERATIONS
                                         )
        return base64.b64encode(pass_hash)

    def compare_password(self, toke1, token2) -> bool:
        return hmac.compare_digest(base64.decode(toke1),
                                   hashlib.pbkdf2_hmac('sha256',
                                                       token2.encode('utf-8'),
                                                       PWD_HASH_SOLT,
                                                       PWD_HASH_ITERATIONS
                                                       )
                                    )

