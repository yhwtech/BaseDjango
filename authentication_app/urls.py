from django.urls import path

from authentication_app.views import login, users, create_user, gestion_user, permissions, \
    GestionPermissionsView

urlpatterns = [
    path('login', login, name='login'),
    path('users', users, name='users'),
    path('users/create/<str:schema_name>', create_user, name='create_user'),
    path('users/<str:schema_name>', gestion_user, name='gestion_user'),
    path('permissions', permissions, name='permissions'),
    path('permissions/<str:group_name>', GestionPermissionsView.as_view(), name='gestion_permissions'),

]

