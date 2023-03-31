from django.urls import path
from .views import (TaskAPIView,
                    TaskUserAPIView,
                    DetailUpdateTaskAPIView,
                    )


urlpatterns = [
        path('project/<int:project_id>/task/<int:task_id>/',
             DetailUpdateTaskAPIView.as_view(),
             name='detail_update_delete'),
        path('project/<int:project_id>/',
             TaskAPIView.as_view(),
             name='task_list_project'),
        path('user/', TaskUserAPIView.as_view(),
             name='task_list_user'),
        ]
