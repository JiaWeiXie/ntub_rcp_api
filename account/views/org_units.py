from rest_framework.permissions import AllowAny
from rest_framework import viewsets
from core.customs.viewsets import CreateRetrieveViewSet
from ..models import OrgUnits
from ..serializers import OrgUnitsSerializer, OrgUnitsRegisterSerializer


class OrgUnitsViewSet(viewsets.ReadOnlyModelViewSet):
    """
    # Mobile API 使用單位/組織API\n
    param org_type(組織單位類型), country(國家), abbreviation(單位縮寫), name(組織單位名稱)\n
    resource get_list, get_detail\n
    method GET
    """
    queryset = OrgUnits.objects.all()
    serializer_class = OrgUnitsSerializer
    permission_classes = (AllowAny,)


class OrgUnitsRegisterViewSet(CreateRetrieveViewSet):
    """
    # WEB API 取得單位/組織API\n
    param org_type(組織單位類型), country(國家), abbreviation(單位縮寫), name(組織單位名稱), created_user(建立人)\n
    resource get_list, get_detail\n
    method GET
    """
    queryset = OrgUnits.objects.all()
    serializer_class = OrgUnitsRegisterSerializer
    permission_classes = (AllowAny,)
