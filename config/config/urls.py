from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/users/', include('users.urls'), name='users'),
    path('api/companies/', include('company.urls'), name='company'),
    path('api/permissions/', include('permissions.urls'), name='permissions'),
    path('api/roles/', include('roles.urls'), name='roles'),
    path('api/projects/', include('projects.urls'), name='projects'),
    path('api/tasks/', include('tasks.urls'), name='tasks'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


# Настройки сайта администратора
admin.site.site_header = 'Админка портфолио'
admin.site.site_title = 'Админка портфолио'
admin.site.index_title = 'Админка портфолио'
