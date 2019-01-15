from .views import *

base_url = 'account'
urlpatterns = []
routers_list = [
    {
        'prefix': r'org_units',
        'viewset': OrgUnitsViewSet,
        'base_name': 'org_units',
    },
    {
        'prefix': r'org_units_register',
        'viewset': OrgUnitsRegisterViewSet,
        'base_name': 'org_units_register',
    },
    {
        'prefix': r'teacher_import',
        'viewset': TeacherImportViewSet,
        'base_name': 'teacher_import',
    },
    {
        'prefix': r'student_import',
        'viewset': StudentImportViewSet,
        'base_name': 'student_import',
    },
    {
        'prefix': r'teacher_detail',
        'viewset': TeacherDetailViewSet,
        'base_name': 'teacher_detail',
    },
    {
        'prefix': r'student_detail',
        'viewset': StudentDetailViewSet,
        'base_name': 'student_detail',
    },
    {
        'prefix': r'users',
        'viewset': UserViewSet,
        'base_name': 'users',
    },
]
