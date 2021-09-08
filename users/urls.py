from django.urls import path
from . import views

urlpatterns = [
    # path("create/", views.register, name="user_create"),
    path('list/', views.UserListView.as_view(), name='user_list'),
    path('create/', views.UserCreateView.as_view(), name='user_create'),
    path('<pk>/update/', views.UserEditView.as_view(), name='user_update'),
    path('<pk>/delete/', views.UserDeleteView.as_view(), name='user_delete'),
]
