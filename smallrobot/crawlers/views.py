import sys
import os
import re 
import importlib 
from .models import *
from background_task import background
from django.http import HttpResponse
from django.shortcuts import render
from django.core.files import File
from django.views.generic import ListView


@background()
def run_crawler(crawler_id, path, args):
    module_name = re.search(r'(?<=/)\w+.py$', path).group(0)
    spec = importlib.util.spec_from_file_location(module_name, path)
    crawler_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(crawler_module)
    result_path = crawler_module.start(**args)
    with open(result_path) as file_result:
        Result(crawler=Crawler.objects.get(id=crawler_id),
            data=File(file_result)).save()
    os.remove(result_path)


class CrawlersList(ListView):
    model = Crawler
    template_name = 'crawlers/crawlers_list.html'

def crawler_runner(request):
    crawlerId = request.GET.get('crawlerid')
    crawler = Crawler.objects.get(id=crawlerId)
    args = {}
    for arg in crawler.args:
        args[arg] = request.GET.get(arg)
    run_crawler(crawler.id, crawler.path, args)
    return HttpResponse("ACK", content_type="text/plain")
    