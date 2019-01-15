from core.customs.viewsets import CreateListRetrieveViewSet

from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ReadOnlyModelViewSet

from .models import RollCallRecord, RollCallCheck, Beacon
from .serializers import RollCallCheckSerializer, RollCallRecordSerializer, BeaconSerializer

from curriculum.models import Subjects, SectionTime
from account.models import is_student, is_teacher


class RollCallCheckViewSet(CreateListRetrieveViewSet):
    """
    新增查詢點名點
    """
    queryset = RollCallCheck.objects.all()
    serializer_class = RollCallCheckSerializer
    permission_classes = [IsAuthenticated]


class RollCallRecordViewSet(ReadOnlyModelViewSet):
    """
    新增查詢點名紀錄
    """
    queryset = RollCallRecord.objects.all()
    serializer_class = RollCallRecordSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if is_teacher(user):
            subjects = Subjects.objects.filter(teacher=user.teacher)
            section_time = SectionTime.objects.filter(subjects__in=subjects)
            queryset = self.queryset.filter(section_time__in=section_time)
        elif is_student(user):
            # subjects = Subjects.objects.filter(members=user.student)
            # section_time = SectionTime.objects.filter(subjects__in=subjects)
            queryset = self.queryset.filter(student=user.student)
        else:
            queryset = self.queryset
        return queryset


class BeaconViewSet(ReadOnlyModelViewSet):
    """
    取得Beacon資訊
    """
    queryset = Beacon.objects.all()
    serializer_class = BeaconSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if is_teacher(user):
            curriculum = Subjects.objects.filter(teacher=user.teacher)
            queryset = self.queryset.filter(curriculum__in=curriculum)
        elif is_student(user):
            curriculum = Subjects.objects.filter(members=user.student)
            queryset = self.queryset.filter(curriculum__in=curriculum)
        else:
            queryset = self.queryset
        return queryset
