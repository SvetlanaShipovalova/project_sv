import unittest
from app.models import User

class UserModelTestCase(unittest.TestCase):
    def test_password_setter(self):
        user = User()
        user.set_password = "hash"
        self.assertTrue(user.password_hash is not None)

    def test_password_no_getter(self):
        user = User()
        user.set_password = "hash"
        with self.assertRaises(AttributeError):
            user.password

    def test_password_verify(self):
        user = User()
        user.set_password = "hash"
        self.assertTrue(user.password_verify("hash"))
        self.assertFalse(user.password_verify("test"))

    def test_salt(self):
        user = User()
        user.set_password = "hash"
        user2 = User()
        user2.set_password = "hash2"
        self.assertTrue(user.password_hash != user2.password_hash)