from django.contrib import admin

from authentication_app.models import Client, License

admin.site.register(Client)
admin.site.register(License)
