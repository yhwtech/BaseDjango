from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect
from django.urls import reverse
from authentication_app.models import Client

@login_required
def base(request):
    return render(request, 'base.html')


@login_required
def home(request):
    client = Client.objects.get(domain_url=request.get_host().split(':')[0])
    return render(request, 'home.html',context={'client':client})


@login_required
@user_passes_test(lambda u: u.is_superuser)
def users(request):
    clients = Client.objects.all()
    if request.method == 'POST':
        selected_client = request.POST.get('client_selected')
        return redirect(reverse('gestion_user', kwargs={'schema_name': selected_client}))
    return render(request, 'users.html', {'clients': clients})


@login_required
def close_session(request):
    logout(request)
    return render(request, 'close_session.html')