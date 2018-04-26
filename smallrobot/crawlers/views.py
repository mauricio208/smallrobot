import sys
import os
import re 
import json 
import importlib
from .models import *

# from background_task import background
from django.conf import settings
from django.shortcuts import render
from django.db import transaction

from django.http import HttpResponse, HttpResponseNotFound, HttpResponseServerError, HttpResponseForbidden
from django.core.files import File
from django.views.generic import ListView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from background_task import background

CRAWLERS_RESULT_DIRPATH = os.path.join(settings.MEDIA_ROOT,"crawlers-results")

@background()
def run_crawler(result_id, args):
    """
    Function that execute crawler code and store result info on the Result table
    param:
    result_id: id of object result where result will be stored
    args: list of arguments used for the crawler call
    """
    result = Result.objects.get(id=result_id)
    path = result.crawler.path
    module_name = re.search(r'(?<=/)\w+.py$', path).group(0)
    spec = importlib.util.spec_from_file_location(module_name, path)
    crawler_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(crawler_module)
    try:
        result_path = crawler_module.start(**args)
        with transaction.atomic():
            with open(result_path) as file_result:
                result.data=File(file_result)
                result.save()
        os.remove(result_path)
    except Exception as e:
        with transaction.atomic():
            result.error=True
            result.error_message=str(e)
            result.save()

@method_decorator(login_required, name='dispatch')
class CrawlersList(ListView):
    model = Crawler
    template_name = 'crawlers/crawlers_list.html'

    def get_queryset(self):
        return Crawler.objects.filter(user=self.request.user)

@login_required
def crawler_runner(request):
    """
    View function that enqueue the crawler execution code in background
    
    return: HttpResponse object with the id of the result
    """
    import pudb; pu.db
    crawler_id = request.GET.get('crawlerid')
    crawler = Crawler.objects.get(id=crawler_id)
    args = {}
    for arg in crawler.args:
        args[arg] = request.GET.get(arg)
    result = Result(crawler=crawler)
    result.save()
    filename = run_crawler(result.id, args)
    # # filename = 'file.csv'
    response = HttpResponse(result.id)
    # response["Content-Disposition"] = "attachment; filename={0}".format(filename)
    # response['X-Accel-Redirect'] = "/crawlers-results/{0}".format(filename)
    return response

@login_required
def download_protected_result(request):
    """
    View function that search for the result file and download it to the user

    return: HttpResponse object with the X-Accel-Redirect header containing the path to the file to be downloaded
    """
    import pudb; pudb.set_trace()
    result_id = request.GET.get('resultid')
    result = Result.objects.get(id=result_id)
    response = HttpResponseForbidden()
    if result.crawler.user == request.user:
        if result.error:
            response = HttpResponseServerError(result.error_message)
        elif not result.data:
            response = HttpResponseNotFound('loading')
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