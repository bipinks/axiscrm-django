from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render

# Create your views here.
from django.utils.dateformat import DateFormat
from django.utils.datetime_safe import datetime

from amc.models import AMCRenewal
from clients.models import Client
from projects.models import Project


def get_all_amc(request):
    filters = {}
    for key, value in request.GET.items():
        if value != '':
            if key == 'client':
                filters["client_project__client"] = value
            if key == 'project':
                filters["client_project__project"] = value
            if key == 'from_date':
                filters["date__gte"] = str(value)
            if key == 'to_date':
                filters["date__lte"] = str(value)

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
