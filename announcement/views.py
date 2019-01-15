from django.utils.timezone import datetime, timedelta

from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from account.models import is_student, is_teacher
from curriculum.models import Subjects

from .serializers import AnnouncementSerializer
from .models import Announcement


class AnnouncementViewSet(ModelViewSet):
    """
    公告新增修改刪除
    """
    queryset = Announcement.objects.all()
    serializer_class = AnnouncementSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if is_teacher(user):
            queryset = self.queryset.filter(created_user=user, end_date__gte=datetime.today())
        elif is_student(user):
            subjects = Subjects.objects.filter(members=user.student)
            queryset = self.queryset.filter(post_target__in=subjects, end_date__gte=datetime.today())
        else:
            queryset = self.queryset.filter(end_date__gte=datetime.today())

        return queryset

