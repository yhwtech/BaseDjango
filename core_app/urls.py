from django.urls import path
from core_app.views import home, close_session
urlpatterns = [
    path('', home, name='home'),
    path('logout', close_session, name='close_session'),
]