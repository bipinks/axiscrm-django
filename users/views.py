from django.contrib.admin.views.decorators import staff_member_required
# views.py
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from my_lib.decorators import class_view_decorator
from .forms import RegisterForm


# Create your views here.
@staff_member_required
def register(response):
    if response.method == "POST":
        form = RegisterForm(response.POST)
        if form.is_valid():
            form.save()
    else:
        form = RegisterForm()

    return render(response, 'common/basic-form.html', {"form": form, 'page_head': "Create User"})


@class_view_decorator(staff_member_required)
class UserCreateView(CreateView):
    model = User
    form_class = RegisterForm
    template_name = 'common/basic-form.html'
    success_url = reverse_lazy('clients_index')
    extra_context = {'page_head': "Create User"}


@class_view_decorator(staff_member_required)
class UserEditView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = RegisterForm
    template_name = 'common/basic-form.html'
    success_url = reverse_lazy('user_list')
    extra_context = {'page_head': "Edit User"}


@class_view_decorator(staff_member_required)
class UserDeleteView(DeleteView):
    model = User
    success_url = reverse_lazy('user_list')


@class_view_decorator(staff_member_required)
class UserListView(ListView):
    model = User
    template_name = 'users/list.html'
    paginate_by = 10
