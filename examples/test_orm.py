import hashlib

from orm.base import Model
from orm import fields


class User(Model):
    username = fields.StringField()
    password = fields.StringField()


def gen_hash(s):
    if hasattr(s, 'encode'):
        s = s.encode('ascii')
    return hashlib.sha256(s).hexdigest()


class SecureUser(Model):
    username = fields.StringField(size=5)
    _password = fields.StringField()

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, pw):
        self._password = gen_hash(pw)

    def check_password(self, pw):
        return self._password == gen_hash(pw)
