from django.test import TestCase
from account.serializers.users import *

import json


class TestUserRegister(TestCase):
    def test_user_signup(self):
        data = """
        {
        "username": "a0001",
        "first_name": "a1",
        "last_name": "n1",
        "password": "123456",
        "email": "user@example.com"
        }
        """
        user_serializer = UserRegisterSerializer(data=json.loads(data))
        self.assertEqual(user_serializer.is_valid(), True)

    def test_user_password_is_hash(self):
        data = """
                {
                "username": "a0001",
                "first_name": "a1",
                "last_name": "n1",
                "password": "123456",
                "email": "user@example.com"
                }
                """
        user_serializer = UserRegisterSerializer(data=json.loads(data))
        user_serializer.is_valid()
        self.assertNotEqual(user_serializer.save().password, '123456')