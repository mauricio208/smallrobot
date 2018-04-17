from django.conf import settings
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.views.generic.base import TemplateView


class LogIn(TemplateView):

    template_name = 'accounts/login.html'
    # def dispatch():
        
    def post(self, *args, **kwargs):
        request = self.request
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect('/crawlers/list')
        render(request, self.template_name, {error:"User doesn't exist, or the is some error on the log in data"})

def log_out(request):
    logout(request)
    return HttpResponseRedirect(settings.LOGIN_URL)