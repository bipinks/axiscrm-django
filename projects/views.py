from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from clients.models import ClientProject, Client
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
