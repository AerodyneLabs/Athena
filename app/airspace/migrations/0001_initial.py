# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.gis.db.models.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AirspaceBase',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('code', models.CharField(max_length=10)),
                ('name', models.CharField(max_length=64)),
                ('effective', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='AirspaceVolume',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('name', models.CharField(max_length=64)),
                ('effective', models.DateField()),
                ('low_altitude', models.FloatField()),
                ('low_agl', models.BooleanField(default=False)),
                ('high_altitude', models.FloatField()),
                ('high_agl', models.BooleanField(default=False)),
                ('boundary', django.contrib.gis.db.models.fields.PolygonField(srid=4326)),
            ],
        ),
        migrations.CreateModel(
            name='Airspace',
            fields=[
                ('airspacebase_ptr', models.OneToOneField(parent_link=True, to='airspace.AirspaceBase', primary_key=True, serialize=False, auto_created=True)),
                ('classification', models.CharField(choices=[('A', 'Class A'), ('B', 'Class B'), ('C', 'Class C'), ('D', 'Class D'), ('E', 'Class E'), ('F', 'Class F'), ('G', 'Class G')], max_length=1)),
            ],
            bases=('airspace.airspacebase',),
        ),
        migrations.CreateModel(
            name='Center',
            fields=[
                ('airspacebase_ptr', models.OneToOneField(parent_link=True, to='airspace.AirspaceBase', primary_key=True, serialize=False, auto_created=True)),
                ('location', django.contrib.gis.db.models.fields.PointField(srid=4326)),
                ('city', models.CharField(max_length=64)),
                ('state', models.CharField(choices=[('AL', 'Alabama'), ('AK', 'Alaska'), ('AS', 'American Samoa'), ('AZ', 'Arizona'), ('AR', 'Arkansas'), ('AA', 'Armed Forces Americas'), ('AE', 'Armed Forces Europe'), ('AP', 'Armed Forces Pacific'), ('CA', 'California'), ('CO', 'Colorado'), ('CT', 'Connecticut'), ('DE', 'Delaware'), ('DC', 'District of Columbia'), ('FL', 'Florida'), ('GA', 'Georgia'), ('GU', 'Guam'), ('HI', 'Hawaii'), ('ID', 'Idaho'), ('IL', 'Illinois'), ('IN', 'Indiana'), ('IA', 'Iowa'), ('KS', 'Kansas'), ('KY', 'Kentucky'), ('LA', 'Louisiana'), ('ME', 'Maine'), ('MD', 'Maryland'), ('MA', 'Massachusetts'), ('MI', 'Michigan'), ('MN', 'Minnesota'), ('MS', 'Mississippi'), ('MO', 'Missouri'), ('MT', 'Montana'), ('NE', 'Nebraska'), ('NV', 'Nevada'), ('NH', 'New Hampshire'), ('NJ', 'New Jersey'), ('NM', 'New Mexico'), ('NY', 'New York'), ('NC', 'North Carolina'), ('ND', 'North Dakota'), ('MP', 'Northern Mariana Islands'), ('OH', 'Ohio'), ('OK', 'Oklahoma'), ('OR', 'Oregon'), ('PA', 'Pennsylvania'), ('PR', 'Puerto Rico'), ('RI', 'Rhode Island'), ('SC', 'South Carolina'), ('SD', 'South Dakota'), ('TN', 'Tennessee'), ('TX', 'Texas'), ('UT', 'Utah'), ('VT', 'Vermont'), ('VI', 'Virgin Islands'), ('VA', 'Virginia'), ('WA', 'Washington'), ('WV', 'West Virginia'), ('WI', 'Wisconsin'), ('WY', 'Wyoming')], max_length=2, blank=True)),
            ],
            bases=('airspace.airspacebase',),
        ),
        migrations.CreateModel(
            name='Navaid',
            fields=[
                ('airspacebase_ptr', models.OneToOneField(parent_link=True, to='airspace.AirspaceBase', primary_key=True, serialize=False, auto_created=True)),
                ('location', django.contrib.gis.db.models.fields.PointField(srid=4326, dim=3)),
                ('city', models.CharField(max_length=64)),
                ('state', models.CharField(choices=[('AL', 'Alabama'), ('AK', 'Alaska'), ('AS', 'American Samoa'), ('AZ', 'Arizona'), ('AR', 'Arkansas'), ('AA', 'Armed Forces Americas'), ('AE', 'Armed Forces Europe'), ('AP', 'Armed Forces Pacific'), ('CA', 'California'), ('CO', 'Colorado'), ('CT', 'Connecticut'), ('DE', 'Delaware'), ('DC', 'District of Columbia'), ('FL', 'Florida'), ('GA', 'Georgia'), ('GU', 'Guam'), ('HI', 'Hawaii'), ('ID', 'Idaho'), ('IL', 'Illinois'), ('IN', 'Indiana'), ('IA', 'Iowa'), ('KS', 'Kansas'), ('KY', 'Kentucky'), ('LA', 'Louisiana'), ('ME', 'Maine'), ('MD', 'Maryland'), ('MA', 'Massachusetts'), ('MI', 'Michigan'), ('MN', 'Minnesota'), ('MS', 'Mississippi'), ('MO', 'Missouri'), ('MT', 'Montana'), ('NE', 'Nebraska'), ('NV', 'Nevada'), ('NH', 'New Hampshire'), ('NJ', 'New Jersey'), ('NM', 'New Mexico'), ('NY', 'New York'), ('NC', 'North Carolina'), ('ND', 'North Dakota'), ('MP', 'Northern Mariana Islands'), ('OH', 'Ohio'), ('OK', 'Oklahoma'), ('OR', 'Oregon'), ('PA', 'Pennsylvania'), ('PR', 'Puerto Rico'), ('RI', 'Rhode Island'), ('SC', 'South Carolina'), ('SD', 'South Dakota'), ('TN', 'Tennessee'), ('TX', 'Texas'), ('UT', 'Utah'), ('VT', 'Vermont'), ('VI', 'Virgin Islands'), ('VA', 'Virginia'), ('WA', 'Washington'), ('WV', 'West Virginia'), ('WI', 'Wisconsin'), ('WY', 'Wyoming')], max_length=2, blank=True)),
                ('variation', models.FloatField()),
                ('service_volume', models.CharField(choices=[('L', 'Low'), ('H', 'High'), ('T', 'Terminal')], max_length=1)),
                ('station_type', models.CharField(choices=[('VOR', 'VOR'), ('DME', 'DME'), ('VOR/DME', 'VOR/DME'), ('VORTAC', 'VORTAC'), ('TACAN', 'TACAN')], max_length=16)),
            ],
            bases=('airspace.airspacebase',),
        ),
        migrations.CreateModel(
            name='Tower',
            fields=[
                ('airspacebase_ptr', models.OneToOneField(parent_link=True, to='airspace.AirspaceBase', primary_key=True, serialize=False, auto_created=True)),
                ('station_type', models.CharField(choices=[('ATCT', 'ATCT'), ('NON-ATCT', 'NON-ATCT'), ('ATCT-A/C', 'ATCT-A/C'), ('ATCT-RAPCON', 'ATCT-RAPCON'), ('ATCT-RATCF', 'ATCT-RATCF'), ('ATCT-TRACON', 'ATCT-TRACON'), ('TRACON', 'TRACON'), ('ATCT-TRACAB', 'ATCT-TRACAB'), ('ATCT-CERAP', 'ATCT-CERAP')], default='NON-ATCT', max_length=16)),
                ('location', django.contrib.gis.db.models.fields.PointField(srid=4326)),
                ('city', models.CharField(max_length=64)),
                ('state', models.CharField(choices=[('AL', 'Alabama'), ('AK', 'Alaska'), ('AS', 'American Samoa'), ('AZ', 'Arizona'), ('AR', 'Arkansas'), ('AA', 'Armed Forces Americas'), ('AE', 'Armed Forces Europe'), ('AP', 'Armed Forces Pacific'), ('CA', 'California'), ('CO', 'Colorado'), ('CT', 'Connecticut'), ('DE', 'Delaware'), ('DC', 'District of Columbia'), ('FL', 'Florida'), ('GA', 'Georgia'), ('GU', 'Guam'), ('HI', 'Hawaii'), ('ID', 'Idaho'), ('IL', 'Illinois'), ('IN', 'Indiana'), ('IA', 'Iowa'), ('KS', 'Kansas'), ('KY', 'Kentucky'), ('LA', 'Louisiana'), ('ME', 'Maine'), ('MD', 'Maryland'), ('MA', 'Massachusetts'), ('MI', 'Michigan'), ('MN', 'Minnesota'), ('MS', 'Mississippi'), ('MO', 'Missouri'), ('MT', 'Montana'), ('NE', 'Nebraska'), ('NV', 'Nevada'), ('NH', 'New Hampshire'), ('NJ', 'New Jersey'), ('NM', 'New Mexico'), ('NY', 'New York'), ('NC', 'North Carolina'), ('ND', 'North Dakota'), ('MP', 'Northern Mariana Islands'), ('OH', 'Ohio'), ('OK', 'Oklahoma'), ('OR', 'Oregon'), ('PA', 'Pennsylvania'), ('PR', 'Puerto Rico'), ('RI', 'Rhode Island'), ('SC', 'South Carolina'), ('SD', 'South Dakota'), ('TN', 'Tennessee'), ('TX', 'Texas'), ('UT', 'Utah'), ('VT', 'Vermont'), ('VI', 'Virgin Islands'), ('VA', 'Virginia'), ('WA', 'Washington'), ('WV', 'West Virginia'), ('WI', 'Wisconsin'), ('WY', 'Wyoming')], max_length=2, blank=True)),
                ('center', models.ForeignKey(null=True, to='airspace.Center', blank=True)),
                ('master', models.ForeignKey(null=True, to='airspace.Tower', blank=True)),
            ],
            bases=('airspace.airspacebase',),
        ),
        migrations.AddField(
            model_name='airspacevolume',
            name='parent',
            field=models.ForeignKey(to='airspace.AirspaceBase', related_name='volumes'),
        ),
    ]
