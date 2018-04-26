import os
import uuid
from django import template
from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import stringfilter

register = template.Library()


class Crawler(models.Model):
    name = models.CharField(max_length=200,  blank=False)
    path = models.TextField(blank=False)
    options = models.TextField()
    user = models.ForeignKey(User, blank=False, on_delete=models.CASCADE)

    @property
    def args(self):
        return [op.strip() for op in self.options.split(',')]
    @property
    def profiles(self):
        return self.profile_set.all()
    # @property
    # def results(self):
    #     return list(self.result_set.filter(data__isnull=False).order_by("-date_time"))
        
class Profile(models.Model):
    crawler = models.ForeignKey('Crawler', blank=False, on_delete=models.CASCADE)
    options = models.TextField()

def crawler_result_path(instance, filename):
    file_extension = os.path.splitext(filename)[1]
    new_filename = str(uuid.uuid1())+file_extension
    return 'crawlers-results/{}'.format(new_filename)

class Result(models.Model):
    crawler = models.ForeignKey('Crawler', on_delete=models.CASCADE)
    data = models.FileField(upload_to=crawler_result_path)
    date_time = models.DateTimeField(auto_now=True)
    error = models.BooleanField(default=False)
    error_message = models.TextField()



