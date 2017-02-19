# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.gis.db.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('atmosphere', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ForecastPoint',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('location', django.contrib.gis.db.models.fields.PointField(dim=3, srid=4326)),
                ('altitude', models.FloatField()),
                ('pressure', models.FloatField()),
                ('temperature', models.FloatField()),
                ('wind_u', models.FloatField()),
                ('wind_v', models.FloatField()),
                ('forecast', models.ForeignKey(to='atmosphere.Forecast')),
            ],
        ),
    ]
