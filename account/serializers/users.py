from rest_framework import serializers

from django.contrib.auth.models import User, Group

import re


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('id', 'name')


class UserDetailSerializer(serializers.ModelSerializer):
    groups = GroupSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email',
                  'is_staff', 'is_active', 'is_superuser',
                  'groups')
        read_only_fields = ('id', 'is_staff', 'is_active', 'is_superuser',
                            'groups')


class UserSerializer(serializers.ModelSerializer):

    def is_valid(self, raise_exception=False):
        user = self.initial_data
        username = user['username']
        if not re.match(r".+@.+\..+\..+", username):
            self._errors = {username: "username format must 'someacount@org_code'."}
            return False
        return super(UserSerializer, self).is_valid(raise_exception)

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email')
        read_only_fields = ('id',)


class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, max_length=128, min_length=6)

    def create(self, validated_data):
        password = validated_data.pop('password')
        model = super(UserRegisterSerializer, self).create(validated_data)
        model.set_password(password)
        model.is_staff = True
        model.save()
        return model

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'password', 'email')
