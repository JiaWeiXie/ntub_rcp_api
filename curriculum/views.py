from django.core.exceptions import ObjectDoesNotExist

from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status, mixins

from account.models import Student, Teacher

from .serializers import SubjectsImportSerializer, SubjectsMembersImportSerializer, \
    SectionTimeImportSerializer, SubjectSectionTimeSerializer

from .models import Subjects, SectionTime


class SubjectsImportViewSet(ModelViewSet):
    """
    # 匯入課表
    """
    queryset = Subjects.objects.all()
    serializer_class = SubjectsImportSerializer
    permission_classes = (IsAuthenticated,)

    def get_serializer(self, *args, **kwargs):

        if self.action == 'create_subjects':
            return self.serializer_class(many=True)

        return super(SubjectsImportViewSet, self).get_serializer(*args, **kwargs)

    @action(methods=['post'], permission_classes=[IsAuthenticated],
            url_path='multi', url_name='multi', detail=False)
    def create_subjects(self, request):
        serializer = self.serializer_class(data=request.data, many=True)
        if serializer.is_valid():
            serializer.save()
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SubjectsStudentImportViewSet(mixins.UpdateModelMixin,
                                   GenericViewSet):
    """
    # 匯入課表人員名單
    members 帶[student_user_id]
    """
    queryset = Subjects.objects.all()
    serializer_class = SubjectsMembersImportSerializer
    permission_classes = (IsAuthenticated,)


class SectionTimeImportViewSet(ModelViewSet):
    """
    # 匯入課表節次
    """
    queryset = SectionTime.objects.all()
    serializer_class = SectionTimeImportSerializer
    permission_classes = (IsAuthenticated,)

    def get_serializer(self, *args, **kwargs):

        if self.action == 'create_section_time':
            return self.serializer_class(many=True)

        return super(SectionTimeImportViewSet, self).get_serializer(*args, **kwargs)

    @action(methods=['post'], permission_classes=[IsAuthenticated],
            url_path='multi', url_name='multi', detail=False)
    def create_section_time(self, request):
        serializer = self.serializer_class(data=request.data, many=True)
        if serializer.is_valid():
            serializer.save()
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def get_student(user):
    try:
        student = Student.objects.get(pk=user.id)
        return student
    except ObjectDoesNotExist:
        return None


def get_teacher(user):
    try:
        teacher = Teacher.objects.get(pk=user.id)
        return teacher
    except ObjectDoesNotExist:
        return None


class SubjectsReadViewSet(mixins.ListModelMixin, GenericViewSet):
    """
    # 瀏覽課表
    """
    serializer_class = SubjectSectionTimeSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):

        class_room = self.request.query_params.get('class_room', None)
        if class_room is not None:
            return Subjects.objects.filter(class_room=class_room, is_active=True)

        user = self.request.user

        if user.is_staff or user.is_superuser:
            return Subjects.objects.all()

        student = get_student(user)
        if student is not None:
            return Subjects.objects.filter(members=student, is_active=True)

        teacher = get_teacher(user)
        if teacher is not None:
            return Subjects.objects.filter(teacher=teacher, is_active=True)

        return Subjects.objects.none()



