from rest_framework.serializers import ModelSerializer

from django.contrib.auth.models import Group

from core.customs.serializers import ExtraRelationModelSerializer, ExtraListSerializer

from ..models import Teacher, User
from .users import UserDetailSerializer, UserSerializer
from .org_units import OrgUnitsSerializer


class ReadOnlyTeacherSerializer(ModelSerializer):
    user = UserDetailSerializer(many=False, read_only=True)
    unit_col = OrgUnitsSerializer(many=False, read_only=True)

    class Meta:
        model = Teacher
        fields = '__all__'


class TeacherSerializer(ExtraRelationModelSerializer):
    user = UserSerializer(many=False, read_only=False, required=True)

    def create(self, validated_data):
        model = super(TeacherSerializer, self).create(validated_data)
        group_name = "{}_teachers".format(model.unit_col.org_code.replace('.', '_'))
        group, _ = Group.objects.get_or_create(name=group_name)
        group.user_set.add(model.user)
        return model

    class Meta:
        model = Teacher
        fields = '__all__'
        extra_models = [(User, 'user')]


class TeacherListSerializer(ExtraListSerializer):
    class Meta:
        extra_serializer_class = TeacherSerializer


class TeacherImportsSerializer(ExtraRelationModelSerializer):
    user = UserSerializer(many=False, read_only=False, required=True)

    def create(self, validated_data):
        model = super(TeacherImportsSerializer, self).create(validated_data)
        group_name = "{}_teachers".format(model.unit_col.org_code.replace('.', '_'))
        group, _ = Group.objects.get_or_create(name=group_name)
        group.user_set.add(model.user)
        return model

    class Meta:
        model = Teacher
        fields = '__all__'
        list_serializer_class = TeacherListSerializer
        extra_models = [(User, 'user')]
