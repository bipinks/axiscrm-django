from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect


# Create your views here.


@login_required
def index(request):
    user = request.user
    if user.is_staff is False:
        return redirect('home_client_dashboard')
    else:
        return render(request, 'home/index.html', {})
