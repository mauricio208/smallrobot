from django.urls import path
from django.views.generic import RedirectView
from . import views

app_name = 'usermanagement'
urlpatterns = [
    path('', RedirectView.as_view(pattern_name='usermanagement:login')),
    path('login', views.LogIn.as_view(), name='login'),
]