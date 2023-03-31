from django.contrib import admin
from .models import Task, TaskFiles


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('id',
                    'name',
                    'project',
                    'company',
                    'author',
                    'executor',
                    'date_sprint',
                    'status'
                    )
    list_display_links = ('name',)
    readonly_fields = ('author',
                       'executor',
                       'project',
                       'company',
                       )


@admin.register(TaskFiles)
class TaskFilesAdmin(admin.ModelAdmin):
    list_display = ('id',
                    'task',
                    'file')
    list_display_links = ('task',)
    readonly_fields = ('task',)
