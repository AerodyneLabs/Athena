# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('airspace', '0002_auto_20150706_0132'),
    ]

    operations = [
        migrations.AddField(
            model_name='tower',
            name='station_type',
            field=models.CharField(choices=[('ATCT', 'ATCT'), ('NON-ATCT', 'NON-ATCT'), ('ATCT-A/C', 'ATCT-A/C'), ('ATCT-RAPCON', 'ATCT-RAPCON'), ('ATCT-RATCF', 'ATCT-RATCF'), ('ATCT-TRACON', 'ATCT-TRACON'), ('TRACON', 'TRACON'), ('ATCT-TRACAB', 'ATCT-TRACAB'), ('ATCT-CERAP', 'ATCT-CERAP')], default='NON-ATCT', max_length=16),
        ),
    ]
