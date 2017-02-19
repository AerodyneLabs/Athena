# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('atmosphere', '0003_remove_forecastpoint_altitude'),
    ]

    operations = [
        migrations.AddField(
            model_name='forecastpoint',
            name='humidity',
            field=models.FloatField(default=None),
            preserve_default=False,
        ),
    ]
