from django.test import TestCase

from account.serializers.org_units import *

import json


class OrgUnitsSerializerTest(TestCase):

    def test_serializer_create(self):
        data = {
            'org_type': 'edu',
            'country': 'tw',
            'abbreviation': 'ntub',
            'name': '臺北商業大學'
        }
        serializer = OrgUnitsSerializer(data=data)
        self.assertEqual(serializer.is_valid(), True)

    def test_serializer_name_blank(self):
        data = {
            'org_type': 'edu',
            'country': 'tw',
            'abbreviation': 'ntub',
            'name': ' 國立 臺北商業大學 '
        }
        serializer = OrgUnitsSerializer(data=data)
        serializer.is_valid()
        self.assertEqual(serializer.validated_data.get('name', None), '國立 臺北商業大學')


class OrgUnitsRegisterSerializerTest(TestCase):
    def setUp(self):
        row_data = """
        {
          "created_user": {
            "username": "teacher001",
            "first_name": "Koa",
            "last_name": "Jacky",
            "password": "123456",
            "email": "user@example.com"
          },
          "org_type": "edu",
          "country": "tw",
          "abbreviation": "shark",
          "name": "SharkOrg"
        }
        """
        self.original_data = json.loads(row_data)

    def test_success_register(self):
        serializer = OrgUnitsRegisterSerializer(data=self.original_data)
        self.assertEqual(serializer.is_valid(raise_exception=True), True)
        self.assertIsNotNone(serializer.save())

    def test_create_fail(self):
        data = self.original_data
        data['created_user']['username'] = None
        serializer = OrgUnitsRegisterSerializer(data=data)
        self.assertEqual(serializer.is_valid(raise_exception=True), False)
        self.assertIsNotNone(serializer.errors)

    def test_org_is_duplicated_fail(self):
        serializer = OrgUnitsRegisterSerializer(data=self.original_data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        self.assertEqual(serializer.is_valid(), False)
        self.assertEqual(serializer.errors, {'org_code': "org_code is duplicated."})
