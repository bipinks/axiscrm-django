from django.contrib.admin.views.decorators import staff_member_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render

# Create your views here.
from django.urls import reverse_lazy
from django.utils.dateformat import DateFormat
from django.utils.datetime_safe import datetime
from django.views.generic import CreateView, DeleteView, UpdateView

from amc.forms import AMCRenewalForm
from amc.models import AMCRenewal
from clients.models import Client
from my_lib.decorators import class_view_decorator
from projects.models import Project


@staff_member_required
def get_all_amc(request):
    filters = {}
    for key, value in request.GET.items():
        if value != '':
            if key == 'client':
                filters["client_project__client"] = value
            if key == 'project':
                filters["client_project__project"] = value
            if key == 'from_date':
                filters["renewed_date__gte"] = str(value)
            if key == 'to_date':
                filters["renewed_date__lte"] = str(value)

    data = AMCRenewal.objects.filter(**filters)

    page = request.GET.get('page', 1)
    paginator = Paginator(data, 5)
    try:
        data = paginator.page(page)
    except PageNotAnInteger:
        data = paginator.page(1)
    except EmptyPage:
        data = paginator.page(paginator.num_pages)

    all_projects = Project.objects.all()
    all_clients = Client.objects.all()
    # print(filters)

    df = DateFormat(datetime.now())
    df.format('Y-m-d')

    return render(request, 'amc/renewal_list.html', {
        "data": data,
        "all_projects": all_projects,
        "all_clients": all_clients,
        "current_date": df.format('Y-m-d'),
    })


@class_view_decorator(staff_member_required)
class AmcCreateView(CreateView):
    model = AMCRenewal
    form_class = AMCRenewalForm
    template_name = 'common/basic-form.html'
    success_url = reverse_lazy('amc_list_all')
    extra_context = {'page_head': "New AMC"}


@class_view_decorator(staff_member_required)
class AmcEditView(UpdateView):
    model = AMCRenewal
    form_class = AMCRenewalForm
    template_name = 'common/basic-form.html'
    success_url = reverse_lazy('amc_list_all')
    extra_context = {'page_head': "Edit AMC"}


@class_view_decorator(staff_member_required)
class AmcDeleteView(DeleteView):
    model = AMCRenewal
    success_url = reverse_lazy('amc_list_all')
