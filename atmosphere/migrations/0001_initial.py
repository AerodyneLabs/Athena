# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Forecast',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('forecast_time', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='ModelRun',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('effective', models.DateTimeField()),
                ('modified', models.DateTimeField()),
                ('spatial_resolution', models.FloatField()),
                ('temporal_resolution', models.DurationField()),
                ('source', models.CharField(max_length=32)),
            ],
        ),
        migrations.AddField(
            model_name='forecast',
            name='model_run',
            field=models.ForeignKey(to='atmosphere.ModelRun'),
        ),
    ]
