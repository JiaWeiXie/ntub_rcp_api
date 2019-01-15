from rest_framework.serializers import ModelSerializer, PrimaryKeyRelatedField


from .models import RollCallCheck, RollCallRecord, Beacon
from curriculum.serializers import SectionTimeSerializer
from account.serializers import ReadOnlyStudentSerializer


class RollCallCheckSerializer(ModelSerializer):
    class Meta:
        model = RollCallCheck
        fields = ('student', 'beacon', 'section_time')
        read_only_fields = ('id',)


class RollCallRecordSerializer(ModelSerializer):
    student = ReadOnlyStudentSerializer(many=False, read_only=True)
    section_time = SectionTimeSerializer(many=False, read_only=True)

    class Meta:
        model = RollCallRecord
        fields = ('record_type', 'record_date', 'section_time', 'student')
        read_only_fields = ('id',)


class BeaconSerializer(ModelSerializer):
    class Meta:
        model = Beacon
        fields = '__all__'
        read_only_fields = ('id',)
