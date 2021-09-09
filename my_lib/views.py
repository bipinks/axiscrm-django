from django.conf import settings
from django.core.mail import send_mail, EmailMessage
from django.shortcuts import render

# Create your views here.
from django.template.loader import get_template
from django.template import Context


def send_email():
    subject = "Sending an email with Django"
    message = "Test Message"

    # send the email to the recipient
    send_mail(subject, message,
              settings.DEFAULT_FROM_EMAIL, ['mr.bipinks@gmail.com'])


def send_template_email(template, ctx):
    message = get_template(template).render(ctx)
    mail = EmailMessage(
        subject="Your Ticket is Submitted",
        body=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=['mr.bipinks@gmail.com'],
        reply_to=['mail@axisproerp.com'],
    )
    mail.content_subtype = "html"
    return mail.send()
