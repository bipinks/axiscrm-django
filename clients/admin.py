from django.contrib import admin
from .models import Client, ClientProject, ClientProjectDocument, SupportRequest, SupportActivity


# Register your models here.
class ClientsAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'address', 'logo')


admin.site.register(Client, ClientsAdmin)


class ClientProjectsAdmin(admin.ModelAdmin):
    list_display = ('client_name', 'project_name', 'start_date', 'description')

    def client_name(self, obj):
        return obj.client.name

    def project_name(self, obj):
        return obj.project.name


admin.site.register(ClientProject, ClientProjectsAdmin)


class ClientProjectDocumentsAdmin(admin.ModelAdmin):
    list_display = ('client_name', 'project_name', 'file', 'description')

    def client_name(self, obj):
        return obj.client_project.client.name

    def project_name(self, obj):
        return obj.client_project.project.name


admin.site.register(ClientProjectDocument, ClientProjectDocumentsAdmin)


class SupportRequestsAdmin(admin.ModelAdmin):
    list_display = ('client_name', 'project_name', 'status', 'description', 'created_at')

    def client_name(self, obj):
        return obj.client_project.client.name

    def project_name(self, obj):
        return obj.client_project.project.name


admin.site.register(SupportRequest, SupportRequestsAdmin)


class SupportActivitiesAdmin(admin.ModelAdmin):
    list_display = ('id', 'client_name', 'project_name', 'description', 'created_at')

    def client_name(self, obj):
        return obj.support_request.client_project.client.name

    def project_name(self, obj):
        return obj.support_request.client_project.project.name


admin.site.register(SupportActivity, SupportActivitiesAdmin)
