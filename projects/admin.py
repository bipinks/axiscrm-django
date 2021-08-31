from django.contrib import admin
from .models import Project


# Register your models here.

class ProjectsAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'logo')


admin.site.register(Project, ProjectsAdmin)
