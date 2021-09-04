from django.contrib import admin

# Register your models here.
from amc.models import AMCRenewal


class AMCRenewalAdmin(admin.ModelAdmin):
    list_display = ('client_name', 'project_name', 'date', 'amount', 'description')
    exclude = ('reference',)

    def client_name(self, obj):
        return obj.client_project.client.name

    def project_name(self, obj):
        return obj.client_project.project.name


admin.site.register(AMCRenewal, AMCRenewalAdmin)
