from django.contrib import admin
from django.urls import path, include
from shared_app.views import my_error_404


urlpatterns = [
    path('admin/', admin.site.urls),
    path('authentication/', include('authentication_app.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', include('core_app.urls')),
]
handler404 = my_error_404

