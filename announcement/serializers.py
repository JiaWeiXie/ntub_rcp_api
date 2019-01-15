from .models import Announcement
from rest_framework.serializers import ModelSerializer


class AnnouncementSerializer(ModelSerializer):

    class Meta:
        model = Announcement
        fields = '__all__'
        read_only_fields = ('post_date',)
