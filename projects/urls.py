from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='projects_index'),

    path('list/', views.ProjectListView.as_view(), name='project_list'),
    path('create/', views.ProjectCreateView.as_view(), name='project_create'),
    path('<pk>/update/', views.ProjectEditView.as_view(), name='project_update'),
    path('<pk>/delete/', views.ProjectDeleteView.as_view(), name='project_delete'),

    # View all projects of a client
    path('view_projects/<client_id>/', views.client_projects, name='project_view_client_projects'),
]
