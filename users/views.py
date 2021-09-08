from django.contrib.admin.views.decorators import staff_member_required
# views.py
from django.shortcuts import render
from .forms import RegisterForm


# Create your views here.
@staff_member_required
def register(response):
    if response.method == "POST":
        form = RegisterForm(response.POST)
        if form.is_valid():
            form.save()
    else:
        form = RegisterForm()

    return render(response, 'common/basic-form.html', {"form": form, 'page_head': "Create User"})
