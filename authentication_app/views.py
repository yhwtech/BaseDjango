from django.contrib.auth.decorators import user_passes_test, login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.models import User, Group, Permission
from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login
from django.urls import reverse
from django.db import connection
from django.views import View
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

@login_required
@user_passes_test(lambda u: u.is_superuser)
def permissions(request):
    groups = Group.objects.all()
    if request.method == 'POST':
        selected_group = request.POST.get('group_selected')
        return redirect(reverse('gestion_permissions', kwargs={'group_id': selected_group}))
    return render(request, 'permissions.html', {'groups': groups})


class GestionPermissionsView(UserPassesTestMixin, View):
    template_name = 'gestion_permissions.html'
    model = Permission
    columns_name= ['Actividad','Permiso']
    columns_model= []
    size_page = 12
    object_permissions_autorization=[]
    def test_func(self):
        return self.request.user.is_superuser

    class Context:
        def __init__(self,
                     model,
                     size_page,
                     columns_name,
                     columns_model,
                     ):
            self.query = model.objects
            self.current_page = 0
            self.records = 0
            self.pages = 0
            self.size_page = size_page
            self.range = range(0, size_page)
            self.columns_name = columns_name
            self.columns_model = columns_model
            self.items = []

        def calc_range_pages(self):
            start_range = max(0, self.current_page - 2)
            end_range = min(start_range + self.size_page, self.pages)

            if end_range - start_range < self.size_page:
                start_range = max(0, end_range - self.size_page)

            self.range = range(start_range, end_range)

        def change_page(self, request, next_page=0,group_id=None):
            tenant_schema = request.tenant.schema_name
            self.current_page = int(next_page)
            with connection.schema_editor(tenant_schema):
                self.records = self.query.count()
                self.pages = (self.records - 1) // self.size_page + 1
                self.calc_range_pages()
                self.build_object_permission(group_id)
                self.items = self.object_permissions_autorization

        def get_permissions(self):
            start_index = self.current_page * self.size_page
            end_index = start_index + self.size_page
            return list(self.query.order_by('id')[start_index:end_index])

        def build_object_permission(self,group_id):
            with schema_context('public'):
                group = Group.objects.get(id=group_id)
                permissions_group = Permission.objects.filter(group=group)
                self.object_permissions_autorization = []
                for permission in self.get_permissions():
                    if permission.id in [permission.id for permission in permissions_group]:
                        authorized = True
                    else:
                        authorized = False
                    self.object_permissions_autorization.append(
                        {"permission": permission, "authorized": authorized})

    def get_context(self, request,group_id):
            context = self.Context(
                model=self.model,
                size_page=self.size_page,
                columns_name=self.columns_name,
                columns_model=self.columns_model,
            )
            if 'page' in request.GET:
                context.change_page(request=request, next_page=request.GET.get('page'),group_id=group_id)
            else:
                context.change_page(request=request,group_id=group_id)
            return context



    def get(self, request, group_id):
        context = self.get_context(request, group_id)
        return render(request, template_name= self.template_name, context=context.__dict__)

    def post(self, request,group_id):
        permissions_change = request.POST['permissions-change'].split('-')
        id_permission = permissions_change[0]
        new_value_permission= permissions_change[1]



        clients = Client.objects.all()
        for client in clients:
            with schema_context(client.schema_name):
                group_change = Group.objects.get(id=group_id)
                if new_value_permission == 'true':
                    group_change.permissions.add(Permission.objects.get(id=int(id_permission)))
                else:
                    group_change.permissions.remove(Permission.objects.get(id=int(id_permission)))
                group_change.save()
        context = self.get_context(request, group_id)

        return render(request=request, template_name= self.template_name, context=context.__dict__)


