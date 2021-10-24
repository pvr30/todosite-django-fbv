from django.contrib import admin
from .models import Task

# Register your models here.
class TaskAdmin(admin.ModelAdmin):
    list_display = ('user', 'task', 'created_date')

admin.site.register(Task, TaskAdmin)