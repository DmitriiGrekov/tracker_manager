from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .serializers import PermissionSerializer
from .models import Permission
from .services import get_permissions

from users.decorators import permit_if_role_in
from users.auth import JWTAuthentication


class PermissionAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = PermissionSerializer
    authentication_classes = (JWTAuthentication,)

    @permit_if_role_in(['pravo-na-prosmotr-prav'])
    def get(self, request):
        """Получение списка прав"""
        permissions = get_permissions()
        serializer = self.serializer_class(permissions, many=True)
        return Response({'data': serializer.data,
                         'status': len(serializer.data)},
                        status=status.HTTP_200_OK)
