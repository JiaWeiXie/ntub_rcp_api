from django.contrib.auth.models import User

from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.viewsets import ViewSet

from ..serializers import UserDetailSerializer


class UserViewSet(ViewSet):
    """
    取得帳號詳細資訊
    """
    queryset = User.objects.all()
    serializer_class = UserDetailSerializer
    permission_classes = (IsAuthenticated,)

    def get_serializer(self, *args, **kwargs):

        if self.action == 'current_detail':
            return self.serializer_class()

        return super(UserViewSet, self).get_serializer(*args, **kwargs)

    @action(methods=['get'], permission_classes=[IsAuthenticated], detail=False)
    def current_detail(self, request):
        try:
            queryset = self.queryset.get(pk=request.user.id)
            serializer = self.serializer_class(queryset)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return Response({'detail': 'Bad request.'}, status=status.HTTP_400_BAD_REQUEST)

