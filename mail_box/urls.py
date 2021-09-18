from django.urls import path
from . import views
from projects import views as project_views

urlpatterns = [
    path('', views.show_mail_box, name="show_mail_box"),
]
