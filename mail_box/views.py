from django.shortcuts import render


# Create your views here.

def show_mail_box(request):
    return render(request, 'mail_box/mail-box.html', {})
