from django.test import TestCase
from ..views import *

import requests


# class OrgUnitsTest(TestCase):
#     def setUp(self):
#         OrgUnits.objects.create(org_type='edu', country='tw',
#                                 abbreviation='ntub', name='臺北商業大學')
#         OrgUnits.objects.create(org_type='edu', country='tw',
#                                 abbreviation='ntu', name='臺灣大學')
#
#     def test_org_units_read_only(self):
#         """
#         測試單位資料取得
#         """
#         pass
