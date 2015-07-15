# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.gis.db.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('airspace', '0003_tower_station_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='navaid',
            name='location',
            field=django.contrib.gis.db.models.fields.PointField(srid=4326, dim=3),
        ),
    ]
