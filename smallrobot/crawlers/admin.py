from django.contrib import admin

from .models import Crawler, Profile

admin.site.register(Crawler)
admin.site.register(Profile)