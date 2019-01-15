from .views import SubjectsImportViewSet, SubjectsStudentImportViewSet, SectionTimeImportViewSet, SubjectsReadViewSet

base_url = 'curriculum'
urlpatterns = []
routers_list = [
    {
        'prefix': r'subjects_import',
        'viewset': SubjectsImportViewSet,
        'base_name': 'subjects_import',
    },
    {
        'prefix': r'students_import',
        'viewset': SubjectsStudentImportViewSet,
        'base_name': 'students_import',
    },
    {
        'prefix': r'section_time_import',
        'viewset': SectionTimeImportViewSet,
        'base_name': 'section_time_import',
    },
    {
        'prefix': r'subjects',
        'viewset': SubjectsReadViewSet,
        'base_name': 'subjects',
    },
]
