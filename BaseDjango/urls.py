from django.contrib import admin
from django.contrib.auth.views import PasswordResetDoneView, PasswordResetCompleteView, PasswordResetConfirmView
from django.urls import path, include

from authentication_app.views import CustomPasswordResetView, login
from shared_app.views import my_error_404


urlpatterns = [
    path('admin/', admin.site.urls),
    path('authentication/', include('authentication_app.urls')),

    path('accounts/password_reset/', CustomPasswordResetView.as_view(), name='password_reset'),
    path('accounts/password_reset/done/', PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('accounts/password/reset/confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(),
         name='password_reset_confirm'),
    path('accounts/password/reset/complete/', PasswordResetCompleteView.as_view(),
         name='password_reset_complete'),
    path('', include('core_app.urls')),
]
handler404 = my_error_404

