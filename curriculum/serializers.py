from rest_framework.serializers import ModelSerializer
from rest_framework import serializers

from core.customs.serializers import ExtraListSerializer, ExtraFieldModelSerializer

from .models import *

from account.models import Student
from account.serializers import UserSerializer

from roll_call.models import Beacon


# 匯入課程序列化
class SubjectsSerializer(ModelSerializer):

    def create(self, validated_data):
        model = super(SubjectsSerializer, self).create(validated_data)
        _ = Beacon.create_beacon(model)
        return model

    class Meta:
        model = Subjects
        exclude = ('create_date', 'is_active', 'members')
        read_only_fields = ('id',)


class SubjectsListSerializer(ExtraListSerializer):
    class Meta:
        extra_serializer_class = SubjectsSerializer


class SubjectsImportSerializer(ModelSerializer):

    def create(self, validated_data):
        model = super(SubjectsImportSerializer, self).create(validated_data)
        _ = Beacon.create_beacon(model)
        return model

    class Meta:
        model = Subjects
        exclude = ('create_date', 'is_active', 'members')
        read_only_fields = ('id',)
        list_serializer_class = SubjectsListSerializer


# 匯入課程名單序列化
class SubjectsStudentsSerializer(ModelSerializer):
    user = UserSerializer(many=False, read_only=True)

    class Meta:
        model = Student
        fields = '__all__'


class SubjectsMembersImportSerializer(ModelSerializer):

    class Meta:
        model = Subjects
        exclude = ('create_date', 'is_active')


# 匯入課程節次序列化
class SectionTimeSerializer(ModelSerializer):
    week = serializers.IntegerField(max_value=7, min_value=1, label='星期')
    section = serializers.IntegerField(min_value=1, label='節次')
    start_time = serializers.TimeField(format='%H:%M', input_formats=['%H:%M'], label='開始時間')
    end_time = serializers.TimeField(format='%H:%M', input_formats=['%H:%M'], label='結束時間')

    class Meta:
        model = SectionTime
        read_only_fields = ('id',)
        fields = '__all__'


class SectionTimeListSerializer(ExtraListSerializer):
    class Meta:
        extra_serializer_class = SectionTimeSerializer


class SectionTimeImportSerializer(ModelSerializer):
    week = serializers.IntegerField(max_value=7, min_value=1, label='星期')
    section = serializers.IntegerField(min_value=1, label='節次')
    start_time = serializers.TimeField(format='%H:%M', input_formats=['%H:%M'], label='開始時間')
    end_time = serializers.TimeField(format='%H:%M', input_formats=['%H:%M'], label='結束時間')

    class Meta:
        model = SectionTime
        fields = '__all__'
        read_only_fields = ('id',)
        list_serializer_class = SectionTimeListSerializer


# Read only Subjects include section time
class SubjectSectionTimeSerializer(ExtraFieldModelSerializer):
    section_times = SectionTimeSerializer(many=True, read_only=True)
    teacher = serializers.StringRelatedField(many=False, read_only=True)

    class Meta:
        model = Subjects
        exclude = ('create_date', 'is_active', 'members')
        extra_fields = ['section_times']
        read_only_fields = ('id',)
