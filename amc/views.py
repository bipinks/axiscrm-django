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
from clients.models import Client, ClientProject
from my_lib.decorators import class_view_decorator
from projects.models import Project

from tablib import Dataset


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


def upload_amc(request):
    if request.method == 'POST':
        dataset = Dataset()
        new_persons = request.FILES['myfile']

        imported_data = dataset.load(new_persons.read(), format='xlsx')
        # print(imported_data)
        for data in imported_data:

            client_name = data[0]
            installation_date = data[1]
            amc_end_date = data[2]
            invoice_amount = data[3]
            amc_amount = data[4]
            amc_start_date = data[5]

            # description = data[2]
            description = "AxisPro Cloud ERP System"
            # project_name = data[3]
            project_name = "AxisPro ERP"

            # check if client exist else create it

            client_object = Client.objects.filter(name=client_name)

            if client_object.exists():
                client_object = client_object.first()
            else:
                client_object = Client(name=client_name, email='no-email@email.com', phone='0123456789',
                                       address="United Arab Emirates")
                client_object.save()

            client_id = client_object.id

            # check if project exist else create it
            project_object = Project.objects.filter(name=project_name)

            # print(project_object)

            if project_object.exists():
                project_object = project_object.first()
            else:
                project_object = Project(name=project_name, description=description)
                project_object.save()

            project_id = project_object.id

            # check if client_project exists else add it
            client_project_object = ClientProject.objects.filter(client_id=client_id, project_id=project_id)
            if client_project_object.exists():
                client_project_object = client_project_object.first()
            else:
                client_project_object = ClientProject(client_id=client_id, project_id=project_id,
                                                      start_date=installation_date,
                                                      next_amc_date=amc_end_date,
                                                      description=description,
                                                      project_amount=invoice_amount,
                                                      amc_amount=amc_amount,
                                                      )
                client_project_object.save()

            client_project_id = client_project_object.id

            # insert amc data
            # amc_object = AMCRenewal(client_project_id=client_project_id,
            #                         start_date=amc_start_date,
            #                         end_date=amc_end_date,
            #                         renewed_date=installation_date,
            #                         description="Amc Renewal AxisPro",
            #                         amount=amc_amount)
            #
            # amc_object.save()

            print(data[1])
            # value = Person(
            #     data[0],
            #     data[1],
            #     data[2],
            #     data[3]
            # )
            # value.save()

            # result = person_resource.import_data(dataset, dry_run=True)  # Test the data import

        # if not result.has_errors():
        #    person_resource.import_data(dataset, dry_run=False)  # Actually import now

    return render(request, 'amc/import_excel.html')
