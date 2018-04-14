# Generated by Django 2.0.4 on 2018-04-11 20:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('crawlers', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Result',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', models.FileField(upload_to='uploads/')),
                ('date_time', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.AddField(
            model_name='crawler',
            name='path',
            field=models.TextField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='result',
            name='crawler',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='crawlers.Crawler'),
        ),
    ]
