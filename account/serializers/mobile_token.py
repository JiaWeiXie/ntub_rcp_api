from rest_framework import serializers
from ..models import DeviceInfo


class MobileTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeviceInfo
        fields = '__all__'
