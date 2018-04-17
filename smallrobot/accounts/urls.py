from django.urls import path, re_path
from django.views.generic import RedirectView
from . import views

app_name = 'accounts'
urlpatterns = [
    path('', RedirectView.as_view(pattern_name='accounts:login')),
    re_path(r'^login', views.LogIn.as_view(), name='login'),
    re_path(r'^logout', views.log_out, name='logout'),
]