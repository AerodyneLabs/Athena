# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('atmosphere', '0002_forecastpoint'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='forecastpoint',
            name='altitude',
        ),
    ]
