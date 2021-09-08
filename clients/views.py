from datetime import datetime

from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import JsonResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.dateformat import DateFormat
from django.utils.decorators import method_decorator
from django.views.generic import DeleteView, UpdateView, CreateView, ListView

from amc.models import AMCRenewal
from lib.decorators import class_view_decorator
from projects.models import Project
from .forms import NewTicketForm, ClientForm
from .models import Client, ClientProject, ClientProjectDocument, SupportRequest, SupportActivity, \
    SupportRequestActivityFiles, SupportRequestFiles, TICKET_STATUS


# Create your views here.

@login_required
@staff_member_required
def index(request):
    clients = Client.objects.all()
    return render(request, 'clients/index.html', {'clients': clients})


@login_required
def project(request, pk):
    project_data = ClientProject.objects.get(pk=pk)
    documents_data = ClientProjectDocument.objects.filter(client_project=project_data)
    support_requests_data = SupportRequest.objects.filter(client_project=project_data)
    amc_data = AMCRenewal.objects.filter(client_project=project_data)

    active_tab = request.GET.get('tab', "overview")

    page = request.GET.get('page', 1)

    # Pagination for Support Request
    paginator = Paginator(support_requests_data, 5)
    try:
        support_requests_data = paginator.page(page)
    except PageNotAnInteger:
        support_requests_data = paginator.page(1)
    except EmptyPage:
        support_requests_data = paginator.page(paginator.num_pages)

    # Pagination for AMC Renewal
    paginator = Paginator(amc_data, 5)
    try:
        amc_data = paginator.page(page)
    except PageNotAnInteger:
        amc_data = paginator.page(1)
    except EmptyPage:
        amc_data = paginator.page(paginator.num_pages)

    data = {"project_data": project_data, "documents_data": documents_data,
            "support_requests_data": support_requests_data,
            "amc_data": amc_data,
            "active_tab": active_tab}
    return render(request, 'clients/client_project_window.html', data)


@login_required
def support_request(request, pk):
    support_request_data = SupportRequest.objects.get(pk=pk)
    support_activity_data = SupportActivity.objects.filter(support_request=support_request_data)
    user_total_service_requests = SupportRequest.objects.filter(created_by=support_request_data.created_by).count()
    return render(request, 'clients/support_request.html', {
        "support_request_data": support_request_data,
        "support_activity_data": support_activity_data,
        "user_total_service_requests": user_total_service_requests
    })


@login_required
@staff_member_required
def get_all_support_requests(request):
    filters = {}
    for key, value in request.GET.items():
        if value != '':
            if key == 'client':
                filters["client_project__client"] = value
            if key == 'project':
                filters["client_project__project"] = value
            if key == 'from_date':
                filters["created_at__date__gte"] = str(value)
            if key == 'to_date':
                filters["created_at__date__lte"] = str(value)

    support_requests_data = SupportRequest.objects.filter(**filters)

    # print(SupportRequest.objects.filter(**filters).query)

    page = request.GET.get('page', 1)

    paginator = Paginator(support_requests_data, 10)
    try:
        support_requests_data = paginator.page(page)
    except PageNotAnInteger:
        support_requests_data = paginator.page(1)
    except EmptyPage:
        support_requests_data = paginator.page(paginator.num_pages)

    all_projects = Project.objects.all()
    all_clients = Client.objects.all()
    # print(filters)

    df = DateFormat(datetime.now())
    df.format('Y-m-d')

    return render(request, 'clients/support_request_list.html', {
        "support_requests_data": support_requests_data,
        "all_projects": all_projects,
        "all_clients": all_clients,
        "ticket_status_dict": TICKET_STATUS,
        "current_date": df.format('Y-m-d'),
    })


@login_required
def save_activity(request):
    if request.is_ajax() and request.method == 'POST':

        description = request.POST.get('description', None)
        request_id = request.POST.get('request_id', None)

        status = "fail"
        msg = "Please check the entered information"

        if description and request_id:

            files = request.FILES.getlist('file')
            activity_model = SupportActivity()
            activity_model.description = description
            activity_model.support_request_id = request_id
            activity_model.save()

            for f in files:
                SupportRequestActivityFiles.objects.create(activity=activity_model, file=f)

            status = "success"
            msg = "Your response is updated"

        return JsonResponse({
            "status": status,
            "msg": msg
        })


# View list of all clients of a project
@login_required
def view_clients(request, project_id):
    project_info = Project.objects.get(pk=project_id)
    project_client_data = ClientProject.objects.filter(project_id=project_id)
    data = {"project_client_data": project_client_data, "project_info": project_info}
    return render(request, 'clients/project_clients.html', data)


@login_required
def new_ticket(request, client_project_id):
    if request.method == "POST":

        ticket_form = NewTicketForm(request.POST, request.FILES)
        ticket_form.client_project = ClientProject.objects.get(pk=client_project_id)
        files = request.FILES.getlist('files')

        if ticket_form.is_valid():
            ticket_object = ticket_form.save()
            for f in files:
                file_instance = SupportRequestFiles(file=f, support_request=ticket_object)
                file_instance.save()

            return JsonResponse({
                "status": "success",
                "msg": "Ticket is submitted",
                "id": ticket_object.id
            })

        return JsonResponse({
            "status": "failed",
            "errors": ticket_form.errors,
            "msg": "Error : Please check the entered data"
        })

    ticket_form = NewTicketForm()
    ticket_form.fields['client_project'].initial = client_project_id
    return render(request, 'clients/new_support_request.html',
                  {'form': ticket_form, 'client_project_id': client_project_id})


@class_view_decorator(staff_member_required)
class SupportRequestDeleteView(DeleteView):
    model = SupportRequest

    @method_decorator(login_required)
    @method_decorator(staff_member_required)
    def delete(self, request, *args, **kwargs):
        self.get_object().delete()
        payload = {
            'status': 'success',
            'msg': 'Support Ticket has been deleted',
        }
        return JsonResponse(payload)


class SupportRequestStatusUpdateView(UpdateView):
    model = SupportRequest

    @method_decorator(login_required)
    @method_decorator(staff_member_required)
    def post(self, request, *args, **kwargs):
        obj = self.get_object()
        obj.status = request.POST["status"]
        obj.save()
        payload = {
            'status': 'success',
            'msg': 'Support Ticket has been updated',
        }
        return JsonResponse(payload)


@class_view_decorator(staff_member_required)
class ClientCreateView(CreateView):
    model = Client
    form_class = ClientForm
    template_name = 'common/basic-form.html'
    success_url = reverse_lazy('clients_index')
    extra_context = {'page_head': "New Client"}


@class_view_decorator(staff_member_required)
class ClientEditView(LoginRequiredMixin, UpdateView):
    model = Client
    form_class = ClientForm
    template_name = 'common/basic-form.html'
    success_url = reverse_lazy('clients_index')
    extra_context = {'page_head': "Edit Client"}


@class_view_decorator(staff_member_required)
class ClientDeleteView(DeleteView):
    model = Client
    success_url = reverse_lazy('clients_index')


@class_view_decorator(staff_member_required)
class ClientListView(ListView):
    model = Client
    template_name = 'clients/list.html'
    paginate_by = 10
