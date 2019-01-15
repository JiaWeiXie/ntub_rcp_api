from django.test import TestCase
from ..models import *


class OrgUnitsTest(TestCase):
    def setUp(self):
        OrgUnits.objects.create(org_type='edu', country='tw',
                                abbreviation='ntub', name='臺北商業大學')
        OrgUnits.objects.create(org_type='edu', country='tw',
                                abbreviation='ntu', name='臺灣大學')

    def test_org_units_integrity(self):
        """
        測試單位資料儲存時是否完整
        """
        swift = OrgUnits(org_type='idv', country='tw',
                         abbreviation='swift', name='臺北商業大學')
        swift.save()
        self.assertEqual(swift.org_type, 'idv')
        self.assertEqual(swift.get_org_code(), 'swift.idv.tw')
        self.assertEqual(swift.org_code, 'swift.idv.tw')

    def test_org_can_get(self):
        """
        測試單位是否能夠正常取得
        """
        ntub = OrgUnits.objects.get(org_code='ntub.edu.tw')
        ntu = OrgUnits.objects.filter(abbreviation='ntu')
        self.assertEqual(ntub.name, '臺北商業大學')
        self.assertEqual(ntu[0].org_code, 'ntu.edu.tw')
