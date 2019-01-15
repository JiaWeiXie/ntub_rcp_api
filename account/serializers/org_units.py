from rest_framework import serializers

from core.customs.serializers import ExtraRelationModelSerializer

from ..models import OrgUnits, User

from .users import UserRegisterSerializer


class OrgUnitsSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrgUnits
        exclude = ('create_date', 'created_user', 'org_uuid')
        read_only_fields = ('org_code',)


class OrgUnitsRegisterSerializer(ExtraRelationModelSerializer):
    created_user = UserRegisterSerializer(many=False, read_only=False, required=True)

    def is_valid(self, raise_exception=False):
        org_data = self.initial_data
        abbreviation = org_data.get('abbreviation', '')
        self.initial_data['abbreviation'] = abbreviation.lower()
        org_type = org_data.get('org_type', '')
        country = org_data.get('country', '')
        org = '{}.{}.{}'.format(abbreviation, org_type, country)
        try:
            OrgUnits.objects.get(org_code=org)
            self._errors = {'org_code': "org_code is duplicated."}
            return False
        except OrgUnits.DoesNotExist:
            return super(OrgUnitsRegisterSerializer, self).is_valid()

    class Meta:
        model = OrgUnits
        exclude = ('create_date',)
        read_only_fields = ('org_code', 'org_uuid')
        extra_models = [(User, 'created_user')]
