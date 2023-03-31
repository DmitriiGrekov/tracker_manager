from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status
from .auth import JWTAuthentication
from .serializers import (RegistrationSerializer,
                          LoginSerializer,
                          UserSerializer,
                          RoleSerializer
                          )
from .renderers import UserJSONRenderer
from .models import User, Role
from .decorators import permit_if_role_in


class RegistrationAPIView(APIView):
    """Регистрация пользователя"""
    permission_classes = (AllowAny,)
    serializer_class = RegistrationSerializer
    renderer_classes = (UserJSONRenderer,)

    def post(self, request):
        """Регистрация пользователя"""
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class LoginAPIView(APIView):
    """Авторизация пользователя"""
    permission_classes = (AllowAny,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = LoginSerializer

    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    """Просмотр и обновление пользователя"""
    permission_classes = (IsAuthenticated,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = UserSerializer
    authentication_classes = (JWTAuthentication,)

    def retrieve(self, request, *args, **kwargs):
        """Получение авторизованного пользователя"""
        serializer = self.serializer_class(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        """Обнолвение пользователя"""
        serialzier_data = request.data
        serializer = self.serializer_class(
                request.user,
                data=serialzier_data,
                partial=True
                )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserProfileAPIVIew(APIView):
    """Получение профиля пользователя"""
    permission_classes = (AllowAny,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = UserSerializer

    def get(self, request,  username):
        """Получеие профиля пользователя"""
        try:
            user = User.objects.get(username=username)
            serializer = self.serializer_class(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'status': 404, 'message': 'Not Found'},
                            status=status.HTTP_404_NOT_FOUND)


class SetUserRoleAPIView(APIView):
    """Устанавливаем роль пользователя"""
    permission_classes = (IsAuthenticated,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = UserSerializer
    authentication_classes = (JWTAuthentication,)

    @permit_if_role_in(['pravo-na-obnovlenie-rolej-polьzovatelyu'])
    def post(self, request, user_id):
        try:
            roles = request.data.get('roles')
            print(roles)
            if not roles:
                return Response({'status': 400, 'message': 'Required params(roles))'},
                                status=status.HTTP_400_BAD_REQUEST)
            user = User.objects.get(id=user_id,
                                    company=request.user.company)
            roles = Role.objects.filter(company=request.user.company,
                                        id__in=list(map(int, request.data.get('roles').split(', '))))
            if roles:
                user.roles.set(roles)
            serializer = self.serializer_class(user)
            return Response(serializer.data,
                            status=status.HTTP_202_ACCEPTED)
        except User.DoesNotExist:
            return Response({'status': 404, 'message': 'Not Found'},
                            status=status.HTTP_404_NOT_FOUND)
