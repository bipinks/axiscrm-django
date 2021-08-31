from datetime import timedelta

from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.shortcuts import render, redirect

# Create your views here.
from django.utils.datetime_safe import datetime

from clients.models import Client, ClientProject, SupportRequest
from projects.models import Project


@login_required
def index(request):
    user = request.user
    if user.is_staff is False:
        return redirect('home_client_dashboard')
    else:

        projects_count = Project.objects.count()
        clients_count = Client.objects.count()

        assigned_projects_count = ClientProject.objects.values("project").annotate(total=Count('id')).count()
        assigned_clients_count = ClientProject.objects.values("client").annotate(total=Count('id')).count()

        unassigned_projects_count = Project.objects.filter(clientproject__isnull=True).count()
        unassigned_clients_count = Project.objects.filter(clientproject__isnull=True).count()

        today = datetime.today()
        end_date = today + timedelta(days=31)
        upcoming_amc_count = ClientProject.objects.filter(next_amc_date__range=[today, end_date]).count()

        amc_due_today_count = ClientProject.objects.filter(next_amc_date=today).count()
        overdue_amc_count = ClientProject.objects.filter(next_amc_date__gt=today).count()

        # print(overdue_amc_count.query)

        total_ticket_count = SupportRequest.objects.count()
        resolved_ticket_count = SupportRequest.objects.filter(status=4).count()
        in_progress_ticket_count = SupportRequest.objects.exclude(status=4).count()
        with_client_review_ticket_count = SupportRequest.objects.filter(status=3).count()

        return render(request, 'home/index.html', {

            "projects_count": projects_count,
            "clients_count": clients_count,

            "assigned_projects_count": assigned_projects_count,
            "assigned_clients_count": assigned_clients_count,
            "unassigned_projects_count": unassigned_projects_count,
            "unassigned_clients_count": unassigned_clients_count,

            "amc_due_today_count": amc_due_today_count,
            "upcoming_amc_count": upcoming_amc_count,
            "overdue_amc_count": overdue_amc_count,

            "total_ticket_count": total_ticket_count,
            "resolved_ticket_count": resolved_ticket_count,
            "in_progress_ticket_count": in_progress_ticket_count,
            "with_client_review_ticket_count": with_client_review_ticket_count,
        })
