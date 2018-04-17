# Generated by Django 2.0.4 on 2018-04-17 06:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('crawlers', '0002_auto_20180411_2001'),
    ]

    operations = [
        migrations.AddField(
            model_name='crawler',
            name='user',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='result',
            name='data',
            field=models.FileField(upload_to='crawlers_results'),
        ),
    ]
