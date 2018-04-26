from django.urls import path
from django.views.generic import RedirectView

from . import views

app_name = 'crawlers'
urlpatterns = [
    path('',RedirectView.as_view(pattern_name='crawlers:crawlers_list')),
    path('list', views.CrawlersList.as_view(), name='crawlers_list'),
    path('run', views.crawler_runner, name='crawler_run'),
    path('result', views.download_protected_result, name='download_protected_result'),
    # path('lastresult', views.crawler_last_result, name='crawler_last_result'),
]