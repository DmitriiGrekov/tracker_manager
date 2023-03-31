from django.contrib import admin
from .models import Project


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'created_at', 'updated_at', 'company',)
    list_display_links = ('name', )
    search_fields = ('name', 'company__name',)
