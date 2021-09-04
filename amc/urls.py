from django.urls import path
from . import views

urlpatterns = [
    path('list/', views.get_all_amc, name='amc_list_all'),

]
