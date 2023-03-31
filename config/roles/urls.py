from django.urls import path
from .views import RoleAPIView, RoleRetrieveUpdateDeleteAPIView


urlpatterns = [
        path('', RoleAPIView.as_view(), name='roles_list'),
        path('<int:role_id>/',
             RoleRetrieveUpdateDeleteAPIView.as_view(),
             name='roles_detail_update_delete'),
        ]
