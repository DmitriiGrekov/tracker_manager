from django.db import IntegrityError
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .serializers import RoleSerializer
from .models import Role
from .exceptions import NoPermissionInRequest
from users.auth import JWTAuthentication
from users.decorators import permit_if_role_in
from permissions.models import Permission
from .services import (get_roles,
                       create_role,
                       get_one_role,
                       update_role,
                       delete_role
                       )


class RoleAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = RoleSerializer
    authentication_classes = (JWTAuthentication,)

    @permit_if_role_in(['pravo-na-prosmotr-rolej'])
    def get(self, request):
        """Вывод списка ролей по компании"""
        roles = get_roles(request.user)
        serializer = self.serializer_class(roles, many=True)
        return Response({'data': serializer.data,
                         'count': len(serializer.data)},
                        status=status.HTTP_200_OK)

    @permit_if_role_in(['pravo-na-dobavlenie-rolej'])
    def post(self, request):
        """Создание ролей компании"""
        try:
            role = create_role(request.data,
                               request.user)
            serializer = self.serializer_class(role)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except NoPermissionInRequest as e:
            return Response({'status': 400, 'message': e.__str__()},
                            status=status.HTTP_400_BAD_REQUEST)
        except IntegrityError as e:
            return Response({'status': 400, 'message': e.__str__()},
                            status=status.HTTP_400_BAD_REQUEST)


class RoleRetrieveUpdateDeleteAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = RoleSerializer
    authentication_classes = (JWTAuthentication,)

    @permit_if_role_in(['pravo-na-prosmotr-rolej'])
    def get(self, request, role_id):
        """Просмотр одной роли"""
        try:
            role = get_one_role(role_id, request.user)
            serializer = self.serializer_class(role)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Role.DoesNotExist:
            return Response({'status': 404, 'message': 'Not Found'},
                            status=status.HTTP_404_NOT_FOUND)

    @permit_if_role_in(['pravo-na-obnovlenie-rolej'])
    def patch(self, request, role_id):
        """Обновление роли"""
        try:
            role = Role.objects.get(pk=role_id,
                                    company=request.user.company)
            role = update_role(request.data,
                               role_id,
                               request.user)
            serializer = self.serializer_class(role)
            return Response(serializer.data,
                            status=status.HTTP_200_OK)
        except Role.DoesNotExist:
            return Response({'status': 404, 'message': 'Not Found'},
                            status=status.HTTP_404_NOT_FOUND)
        except IntegrityError as e:
            return Response({'status': 400, 'message': e.__str__()},
                            status=status.HTTP_400_BAD_REQUEST)
        except NoPermissionInRequest as e:
            return Response({'status': 400, 'message': e.__str__()},
                            status=status.HTTP_400_BAD_REQUEST)

    @permit_if_role_in(['pravo-na-udalenie-rolej'])
    def delete(self, request, role_id):
        """Удаление роли"""
        try:
            delete_role(role_id, request.user)
            return Response({'status': True,
                             'message': 'Success'},
                            status=status.HTTP_204_NO_CONTENT)
        except Role.DoesNotExist:
            return Response({'status': 404, 'message': 'Not Found'},
                            status=status.HTTP_404_NOT_FOUND)
