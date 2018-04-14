from django.urls import path

from . import views

app_name = 'crawlers'
urlpatterns = [
    path('list', views.CrawlersList.as_view(), name='crawlers_list'),
    path('run', views.crawler_runner, name='crawler_run'),
]