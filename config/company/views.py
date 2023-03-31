from django.contrib.contenttypes.models import ContentType
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from .serializers import CompanySerializer
from .models import Company
from .exceptions import NoUserDataInRequest, NotFoundEmailData
from .services import (get_user_company,
                       create_company,
                       update_company,
                       delete_company,
                       add_user_in_company,
                       delete_user_from_company
                       )
from users.auth import JWTAuthentication
from users.models import User
from roles.models import Role
from permissions.models import Permission
from users.decorators import permit_if_role_in


class CompanyAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = CompanySerializer
    authentication_classes = (JWTAuthentication,)

    @permit_if_role_in(['pravo-na-prosmotr-kompanii'])
    def get(self, request):
        """Получение компании в которой учавствует пользователь"""
        companies = get_user_company(request.user)
        serializer = self.serializer_class(companies, many=True)
        return Response({'data': serializer.data,
                         'status': len(serializer.data)}, status=status.HTTP_200_OK)

    def post(self, request):
        """Создание компании"""
        company = create_company(request.data,
                                 request.user)
        serializer = self.serializer_class(company)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CompanyRetrieveUpdateAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = CompanySerializer
    authentication_classes = (JWTAuthentication,)

    @permit_if_role_in(['pravo-na-obnovlenie-kompanij'])
    def patch(self, request, company_id):
        """Обновление компании"""
        try:
            company = update_company(request.data,
                                     company_id,
                                     request.user)
            serializer = self.serializer_class(company)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Company.DoesNotExist:
            return Response({'status': 404, 'message': 'Not found'},
                            status=status.HTTP_404_NOT_FOUND)

    @permit_if_role_in(['pravo-na-udalenie-kompanij'])
    def delete(self, request, company_id):
        """Удаление компании автором"""
        try:
            delete_company(company_id, request.user)
            return Response({'status': 200, 'message': 'Success'},
                            status=status.HTTP_204_NO_CONTENT)
        except Company.DoesNotExist:
            return Response({'status': 404, 'message': 'Not found'},
                            status=status.HTTP_404_NOT_FOUND)


class AddCompanyUsers(APIView):
    """Добавление людей в компанию"""
    permission_classes = (IsAuthenticated,)
    serializer_class = CompanySerializer
    authentication_classes = (JWTAuthentication,)

    @permit_if_role_in(['provo-na-dobavlenie-lyudej-v-kompaniyu'])
    def post(self, request):
        """Добавление людей в компанию"""
        try:
            users_emails = request.data.get('users_emails')
            add_user_in_company(request.user,
                                users_emails)
            return Response({'status': 200, 'message': 'Success add user'},
                            status=status.HTTP_200_OK)
        except Company.DoesNotExist:
            return Response({'status': 404, 'message': 'Not found'},
                            status=status.HTTP_404_NOT_FOUND)
        except NotFoundEmailData as e:
            return Response({'status': 400, 'message': e.__str__()},
                            status=status.HTTP_400_BAD_REQUEST)


class DeleteCompanyUsers(APIView):
    """Добавление людей в компанию"""
    permission_classes = (IsAuthenticated,)
    serializer_class = CompanySerializer
    authentication_classes = (JWTAuthentication,)

    @permit_if_role_in(['pravo-na-udalenie-lyudej-iz-kompaniyu'])
    def post(self, request):
        """Удаление людей из компании"""
        try:
            users_emails = request.data.get('users_emails')
            delete_user_from_company(request.user,
                                     users_emails)
            return Response({'status': 200, 'message': 'Success delete user'},
                            status=status.HTTP_200_OK)
        except Company.DoesNotExist:
            return Response({'status': 404, 'message': 'Not found'},
                            status)
        except NotFoundEmailData as e:
            return Response({'status': 400, 'message': e.__str__()},
                            status=status.HTTP_400_BAD_REQUEST)
