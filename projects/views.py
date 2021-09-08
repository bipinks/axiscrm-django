from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import UpdateView, CreateView, DeleteView, ListView

from clients.models import ClientProject, Client
from lib.decorators import class_view_decorator
from .forms import ProjectForm
from .models import Project


# Create your views here.
@login_required
@staff_member_required
def index(request):
    projects = Project.objects.all()
    return render(request, 'projects/index.html', {'projects': projects})


# View list of all projects of client
@login_required
@staff_member_required
def client_projects(request, client_id):
    client_info = get_client_info(client_id)
    client_projects_data = get_client_projects(client_id)

    data = {"client_projects_data": client_projects_data, "client_info": client_info}
    return render(request, 'projects/client_projects.html', data)


def client_dashboard(request):
    client = request.user.client
    if client is not None:
        client_id = client.id
        client_info = get_client_info(client_id)
        client_projects_data = get_client_projects(client_id)

        data = {"client_projects_data": client_projects_data, "client_info": client_info}
        return render(request, 'projects/client_projects.html', data)


def get_client_projects(client_id):
    client_projects_data = ClientProject.objects.filter(client_id=client_id)
    return client_projects_data


def get_client_info(client_id):
    client_info = Client.objects.get(pk=client_id)
    return client_info


@class_view_decorator(staff_member_required)
class ProjectCreateView(CreateView):
    model = Project
    form_class = ProjectForm
    template_name = 'common/basic-form.html'
    success_url = reverse_lazy('projects_index')
    extra_context = {'page_head': "New Project"}


@class_view_decorator(staff_member_required)
class ProjectEditView(UpdateView):
    model = Project
    form_class = ProjectForm
    template_name = 'common/basic-form.html'
    success_url = reverse_lazy('projects_index')
    extra_context = {'page_head': "Edit Project"}


@class_view_decorator(staff_member_required)
class ProjectDeleteView(DeleteView):
    model = Project
    success_url = reverse_lazy('clients_index')


@class_view_decorator(staff_member_required)
class ProjectListView(ListView):
    model = Project
    template_name = 'projects/list.html'
    paginate_by = 10
