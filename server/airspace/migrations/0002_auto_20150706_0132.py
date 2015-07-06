# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('airspace', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tower',
            name='center',
            field=models.ForeignKey(null=True, blank=True, to='airspace.Center'),
        ),
    ]
