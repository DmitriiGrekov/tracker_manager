from django.urls import path
from .views import PermissionAPIView


urlpatterns = [
        path('', PermissionAPIView.as_view(), name='permissions_list'),
        ]
