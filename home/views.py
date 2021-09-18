from datetime import timedelta

from django.contrib.auth.decorators import login_required
from django.db import connection
from django.db.models import Count
from django.http import JsonResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.utils.datetime_safe import datetime
from django_mailbox.models import Mailbox, Message

from clients.models import Client, ClientProject, SupportRequest
from my_lib.views import send_email, send_template_email, dict_fetch_all
from projects.models import Project


@login_required
def index(request):
    # send_email()
    # send_template_email()

    # mail_t = Message.objects.get(pk=1)
    #
    # print(mail_t)

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
        overdue_amc_count = ClientProject.objects.filter(next_amc_date__lt=today).count()

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


def get_next_year_amc_data(request):
    sql = 'SELECT p.name project_name,COUNT(DISTINCT(p.id)) projects_cnt,' \
          'COUNT(DISTINCT(c.id)) clients_cnt,SUM(cp.amc_amount) sum_amc_amount ' \
          'FROM client_projects cp LEFT JOIN projects p ON p.id=cp.project_id ' \
          'LEFT JOIN clients c ON c.id=cp.client_id ' \
          'WHERE cp.next_amc_date >= CURDATE() AND cp.next_amc_date < (DATE_ADD(CURDATE(), INTERVAL 1 YEAR)) ' \
          'GROUP BY cp.project_id'

    cursor = connection.cursor()
    cursor.execute(sql)
    row = dict_fetch_all(cursor)

    return JsonResponse({
        "status": "OK",
        "data": row
    })
