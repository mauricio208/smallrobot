from django.urls import path

from . import views

app_name = 'crawlers'
urlpatterns = [
    path(r'list', views.CrawlersList.as_view(), name='crawlers_list'),
    path('run', views.crawler_runner, name='crawler_run'),
    path('lastresult', views.crawler_last_result, name='crawler_last_result'),
]