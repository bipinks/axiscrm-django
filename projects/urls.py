from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='projects_index'),

    # View all projects of a client
    path('view_projects/<client_id>/', views.client_projects, name='project_view_client_projects'),
]
