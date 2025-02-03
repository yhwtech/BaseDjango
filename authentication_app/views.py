from django.contrib.auth.decorators import user_passes_test, login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm
from django.contrib.auth.models import User, Group, GroupManager
from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login
from django.urls import reverse
from tenant_schemas.utils import schema_context

from authentication_app.models import Client


# Create your views here.
def login(request):
    form = AuthenticationForm(request, data=request.POST or None)
    if form.is_valid():
        auth_login(request, form.get_user())
        return redirect('home')
    return render(request, 'registration/login.html', {'form': form})


@user_passes_test(lambda u: u.is_superuser)
def gestion_user(request, schema_name):
    with schema_context(schema_name):
        users_db = User.objects.all()
        return render(request, 'gestion_user.html', {'users': users_db, 'schema_name': schema_name})


@user_passes_test(lambda u: u.is_superuser)
def create_user(request, schema_name):
    with schema_context(schema_name):
        users_db = User.objects.all()
        groups_db = Group.objects.all()
        if request.method == 'POST':
            group_id = request.POST['group']
            form = UserCreationForm(request.POST)
            if form.is_valid():
                user = form.save(commit=False)
                user.set_password(form.cleaned_data['password1'])
                user.save()
                user_complete = UserChangeForm(request.POST, instance=user)
                if user_complete.is_valid():
                    user_complete.save()
                    group = Group.objects.get(id=group_id)
                    group.user_set.add(user)
                    return redirect(reverse('gestion_user', kwargs={'schema_name': schema_name}))

        else:
            form = UserCreationForm()
        return render(request, 'create_user.html',
                      {
                          'form': form,
                          'schema_name': schema_name,
                          'users': users_db,
                          'groups': groups_db,
                      })

@login_required
@user_passes_test(lambda u: u.is_superuser)
def users(request):
    clients = Client.objects.all()
    if request.method == 'POST':
        selected_client = request.POST.get('client_selected')
        return redirect(reverse('gestion_user', kwargs={'schema_name': selected_client}))
    return render(request, 'users.html', {'clients': clients})