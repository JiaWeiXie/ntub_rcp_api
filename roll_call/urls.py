from .views import *

base_url = 'roll_call'
urlpatterns = []
routers_list = [
    {
        'prefix': r'roll_call_check',
        'viewset': RollCallCheckViewSet,
        'base_name': 'roll_call_check',
    },
    {
        'prefix': r'roll_call_record',
        'viewset': RollCallRecordViewSet,
        'base_name': 'roll_call_record',
    },
    {
        'prefix': r'beacons',
        'viewset': BeaconViewSet,
        'base_name': 'beacons',
    },
]
