from django.urls import path
from . import views

urlpatterns = [

    path('create/', views.AmcCreateView.as_view(), name='amc_create'),
    path('<pk>/update/', views.AmcEditView.as_view(), name='amc_update'),
    path('<pk>/delete/', views.AmcDeleteView.as_view(), name='amc_delete'),

    path('list/', views.get_all_amc, name='amc_list_all'),

]
