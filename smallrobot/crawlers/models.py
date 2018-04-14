from django.db import models

class Crawler(models.Model):
    name = models.CharField(max_length=200,  blank=False)
    path = models.TextField(blank=False)
    options = models.TextField()

    @property
    def args(self):
        return [op.strip() for op in self.options.split(',')]
    
    @property
    def results(self):
        return list(self.result_set.filter(data__isnull=False).order_by("-date_time"))

class Result(models.Model):
    crawler = models.ForeignKey('Crawler', blank=False, on_delete=models.CASCADE)
    data = models.FileField(upload_to='crawlers_results')
    date_time = models.DateTimeField(auto_now=True)



