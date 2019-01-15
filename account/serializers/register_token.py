from rest_framework import serializers
from ..models import RegisterToken


class RegisterTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegisterToken
        exclude = ('create_date',)
