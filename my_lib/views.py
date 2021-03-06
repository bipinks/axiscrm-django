from django.conf import settings
from django.core.mail import send_mail, EmailMessage

# Create your views here.
from django.template.loader import get_template
from django.utils import timezone
from django.utils.dateformat import DateFormat
from datetime import datetime, timedelta




def send_email():
    subject = "Sending an email with Django"
    message = "Test Message"

    # send the email to the recipient
    send_mail(subject, message,
              settings.DEFAULT_FROM_EMAIL, ['mr.bipinks@gmail.com'])


def send_template_email(template, ctx):
    cc = []
    bcc = ['mr.bipinks@gmail.com']

    subject = ctx["email_subject"]
    to = [ctx["to_email"]]
    from_email = f'Support <{settings.DEFAULT_FROM_EMAIL}>'
    reply_to = [f'Support <{settings.DEFAULT_FROM_EMAIL}>']

    message = get_template(template).render(ctx)
    mail = EmailMessage(
        subject=subject,
        body=message,
        from_email=from_email,
        to=to,
        reply_to=reply_to,
        cc=cc,
        bcc=bcc
    )
    mail.content_subtype = "html"
    return mail.send()


def get_current_date():
    df = DateFormat(datetime.now())
    df.format('Y-m-d')
    return df.format('Y-m-d')


def date_to_sql(date):
    df = DateFormat(date)
    df.format('Y-m-d')
    return df.format('Y-m-d')


def date_next_year():
    now = timezone.now()
    return now + timedelta(days=365)


def date_add_days(days):
    now = timezone.now()
    return now + timedelta(days=days)


def dict_fetch_all(cursor):
    """Return all rows from a cursor as a dict"""
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]
