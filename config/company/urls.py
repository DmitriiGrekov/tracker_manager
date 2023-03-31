from django.urls import path
from .views import (CompanyAPIView,
                    CompanyRetrieveUpdateAPIView,
                    AddCompanyUsers,
                    DeleteCompanyUsers,
                    )


urlpatterns = [
        path('', CompanyAPIView.as_view(), name='list_create'),
        path('<int:company_id>/',
             CompanyRetrieveUpdateAPIView.as_view(),
             name='retrieve_update'),
        path('add/user/',
             AddCompanyUsers.as_view(),
             name='add_user_in_company'),
        path('delete/user/',
             DeleteCompanyUsers.as_view(),
             name='delete_user_in_company'),
        ]
