from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

from core.customs.viewsets import CreateListRetrieveViewSet, RetrieveViewSet

from ..models import Teacher
from ..serializers import TeacherImportsSerializer, ReadOnlyTeacherSerializer


class TeacherImportViewSet(CreateListRetrieveViewSet):
    """
    # WEB API 教師資料多筆匯入
    """
    queryset = Teacher.objects.all()
    serializer_class = TeacherImportsSerializer
    permission_classes = (IsAuthenticated,)

    def get_serializer(self, *args, **kwargs):

        if self.action == 'create_teachers':
            return self.serializer_class(many=True)

        return super(TeacherImportViewSet, self).get_serializer(*args, **kwargs)

    @action(methods=['post'], permission_classes=[IsAuthenticated, ],
            url_path='multi', url_name='multi', detail=False)
    def create_teachers(self, request):
        serializer = self.serializer_class(data=request.data, many=True)
        if serializer.is_valid():
            serializer.save()
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TeacherDetailViewSet(RetrieveViewSet):
    """
    # Mobile API 取得教師帳號詳細資訊
    """
    queryset = Teacher.objects.all()
    serializer_class = ReadOnlyTeacherSerializer
    permission_classes = (IsAuthenticated,)
