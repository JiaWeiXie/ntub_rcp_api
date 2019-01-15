from django.test import TestCase
from account.serializers.teachers import *
from account.models import OrgUnits


class TeacherRegisterSerializerTest(TestCase):
    def setUp(self):
        self.ntub = OrgUnits.objects.create(org_type='edu', country='tw',
                                            abbreviation='ntub', name='臺北商業大學')
        self.ntu = OrgUnits.objects.create(org_type='edu', country='tw',
                                           abbreviation='ntu', name='臺灣大學')

    def test_register_teacher(self):
        user = {
            'username': '10446005@ntub.edu.tw',
            'first_name': 'Jason',
            'last_name': 'Xie',
            'email': '10446005@ntub.edu.tw',
        }
        teacher = TeacherSerializer(data={
            'user': user,
            'department': '資管系',
            'time_case': '專任',
            'job_title': '助教',
            'unit_col': self.ntub.org_code,
        })
        teacher.is_valid()
        self.assertEqual(bool(teacher.save()), True)

    def test_valid_eroor(self):
        user = {
            'first_name': 'Jason',
            'last_name': 'Xie',
            'email': '10446005@ntub.edu.tw',
        }
        teacher = TeacherSerializer(data={
            'user': user,
            'department': '資管系',
            'time_case': '專任',
            'job_title': '助教',
            'unit_col': self.ntub.org_code,
        })
        self.assertEqual(teacher.is_valid(), False)