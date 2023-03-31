from django.urls import path
from .views import (ProjectAPIView,
                    DetailUpdateDeleteAPIView,
                    UpdateUserInProject
                    )


urlpatterns = [
        path('', ProjectAPIView.as_view(), name='projects_list'),
        path('<int:project_id>/users',
             UpdateUserInProject.as_view(),
             name='user_project_update'),
        path('<int:project_id>/',
             DetailUpdateDeleteAPIView.as_view(),
             name='detail_update_delete'),
        ]
