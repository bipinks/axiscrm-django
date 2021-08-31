from django.urls import path
from . import views
from .views import SupportRequestDeleteView, SupportRequestUpdateView

urlpatterns = [
    path('', views.index, name='clients_index'),
    path('view_project/<pk>/', views.project, name="clients_view_project"),
    path('support_request/<pk>/', views.support_request, name="clients_view_support_request"),
    path('save_activity', views.save_activity, name='post_support_activity'),

    # View all clients of a project
    path('view_clients/<project_id>/', views.view_clients, name="projects_view_project_clients"),
    path('all_support_requests/', views.get_all_support_requests, name='clients_all_support_requests'),
    path('view_project/<client_project_id>/new_ticket/', views.new_ticket, name='clients_new_ticket'),

    path('<pk>/deleteTicket/', SupportRequestDeleteView.as_view(), name='delete_support_ticket'),
    path('<pk>/updateTicket', SupportRequestUpdateView.as_view(), name='update_support_ticket'),

]
