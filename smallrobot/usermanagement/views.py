from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.views.generic.base import TemplateView


class LogIn(TemplateView):

    template_name = 'usermanagement/login.html'

    def post(self, **kwargs):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect('/crawlers/list')
        render(request, self.template_name, {error:"User doesn't exist, or the is some error on the log in data"})