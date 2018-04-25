import sys
import os
import re 
import json 
import importlib
from .models import *

# from background_task import background
from django.conf import settings
from django.http import HttpResponse, HttpResponseServerError, HttpResponseForbidden
from django.shortcuts import render
from django.core.files import File
from django.views.generic import ListView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from background_task import background

CRAWLERS_RESULT_DIRPATH = os.path.join(settings.MEDIA_ROOT,"crawlers-results")

@background()
def run_crawler(result_id, args):
    result = Result.objects.get(id=result_id)
    path = result.crawler.path
    module_name = re.search(r'(?<=/)\w+.py$', path).group(0)
    spec = importlib.util.spec_from_file_location(module_name, path)
    crawler_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(crawler_module)
    try:
        result_path = crawler_module.start(**args)
        with open(result_path) as file_result:
            result.data=File(file_result)
        os.remove(result_path)
    except expression as e:
        result.error=True
        result.error_message=str(e)
    result.save()
    # file_extension = os.path.splitext(result_path)[1]
    # new_filename = str(uuid.uuid1())+file_extension
    # new_path = os.path.join(CRAWLERS_RESULT_DIRPATH, new_filename)
    # os.rename(result_path, new_path)

@method_decorator(login_required, name='dispatch')
class CrawlersList(ListView):
    model = Crawler
    template_name = 'crawlers/crawlers_list.html'

    def get_queryset(self):
        return Crawler.objects.filter(user=self.request.user)

@login_required
def crawler_runner(request):
    import pudb; pu.db
    crawler_id = request.GET.get('crawlerid')
    crawler = Crawler.objects.get(id=crawler_id)
    args = {}
    for arg in crawler.args:
        args[arg] = request.GET.get(arg)
    result = Result(crawler=crawler).save()
    filename = run_crawler(result.id, args)
    # # filename = 'file.csv'
    response = HttpResponse(result.id)
    # response["Content-Disposition"] = "attachment; filename={0}".format(filename)
    # response['X-Accel-Redirect'] = "/crawlers-results/{0}".format(filename)
    return response

@login_required
def download_protected_result(request):
    result_id = request.Get.get('resultid')
    result = Result.objects.get(id=result_id)
    response = HttpResponseForbidden()
    if result.crawler.user == request.user:
        if result.error:
            response = HttpResponseServerError(result.error_message)
        else:
            filename = os.path.basename(result.data.name)
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
def delete_profile(request):
    profile_id = request.POST.get('profileid')
    Profile.objects.get(id=profile_id).delete()
    return HttpResponse('Profile deleted')