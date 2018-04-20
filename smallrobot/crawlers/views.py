import sys
import os
import re 
import json 
import uuid
import importlib
from .models import *
# from background_task import background
from django.conf import settings
from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render
from django.core.files import File
from django.views.generic import ListView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

CRAWLERS_RESULT_DIRPATH = os.path.join(settings.MEDIA_ROOT,"crawlers-results")

def run_crawler(crawler_id, path, args):
    module_name = re.search(r'(?<=/)\w+.py$', path).group(0)
    spec = importlib.util.spec_from_file_location(module_name, path)
    crawler_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(crawler_module)
    result_path = crawler_module.start(**args)
    file_extension = os.path.splitext(result_path)[1]
    new_filename = str(uuid.uuid1())+file_extension
    new_path = os.path.join(CRAWLERS_RESULT_DIRPATH, new_filename)
    os.rename(result_path, new_path)
    return new_filename

@method_decorator(login_required, name='dispatch')
class CrawlersList(ListView):
    model = Crawler
    template_name = 'crawlers/crawlers_list.html'

    def get_queryset(self):
        return Crawler.objects.filter(user=self.request.user)

@login_required
def crawler_runner(request):
    crawlerId = request.GET.get('crawlerid')
    crawler = Crawler.objects.get(id=crawlerId)
    args = {}
    for arg in crawler.args:
        args[arg] = request.GET.get(arg)
    filename = run_crawler(crawler.id, crawler.path, args)
    response = HttpResponse()
    response["Content-Disposition"] = "attachment; filename={0}".format(filename)
    response['X-Accel-Redirect'] = "/crawlers-results/{0}".format(filename)
    return response

# @login_required
# def crawler_last_result(request):
#     crawlerId = request.GET.get('crawlerid')
#     crawler = Crawler.objects.get(id=crawlerId)
#     data = crawler.result_set.last()
#     data = {'id':data.id, 'url':data.data.url, 'dateTime': str(data.date_time)}
#     return HttpResponse(json.dumps(data), content_type="application/json")