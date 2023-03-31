from django.urls import path
from .views import (RegistrationAPIView,
                    LoginAPIView,
                    UserRetrieveUpdateAPIView,
                    UserProfileAPIVIew,
                    SetUserRoleAPIView,
                    )

urlpatterns = [
    path('register/', RegistrationAPIView.as_view(), name='register'),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('', UserRetrieveUpdateAPIView.as_view(), name='retrieve_update'),
    path('profile/<str:username>/',
         UserProfileAPIVIew.as_view(),
         name='user_profile'),
    path('<int:user_id>/set/role/',
         SetUserRoleAPIView.as_view(),
         name='set_role'),
    ]
