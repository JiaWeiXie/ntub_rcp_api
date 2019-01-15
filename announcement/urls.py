from .views import *

base_url = 'announcement'
urlpatterns = []
routers_list = [
    {
        'prefix': r'posts',
        'viewset': AnnouncementViewSet,
        'base_name': 'posts',
    },
]
