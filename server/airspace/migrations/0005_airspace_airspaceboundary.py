# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.gis.db.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('airspace', '0004_auto_20150715_0410'),
    ]

    operations = [
        migrations.CreateModel(
            name='Airspace',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('name', models.CharField(max_length=64, unique=True)),
                ('effective', models.DateField()),
                ('classification', models.CharField(max_length=1, choices=[('A', 'Class A'), ('B', 'Class B'), ('C', 'Class C'), ('D', 'Class D'), ('E', 'Class E'), ('F', 'Class F'), ('G', 'Class G')])),
            ],
        ),
        migrations.CreateModel(
            name='AirspaceBoundary',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('effective', models.DateField()),
                ('low_altitude', models.FloatField()),
                ('high_altitude', models.FloatField()),
                ('boundary', django.contrib.gis.db.models.fields.PolygonField(srid=4326)),
                ('airspace', models.ForeignKey(to='airspace.Airspace')),
            ],
        ),
    ]
