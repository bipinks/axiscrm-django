from django.urls import path
from . import views
from projects import views as project_views

urlpatterns = [
    path('', views.index, name="home_index"),
    path('c_dashboard/', project_views.client_dashboard, name="home_client_dashboard"),
    path('next_year_amc_data/', views.get_next_year_amc_data, name="home_next_year_amc_data")
]
