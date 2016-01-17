from django.contrib.gis.db import models
from localflavor.us.us_states import STATE_CHOICES
from airspace.models import AirspaceBase

class Tower(AirspaceBase):

    # Constants
    ATCT = 'ATCT'
    NON_ATCT = 'NON-ATCT'
    ATCT_AC = 'ATCT-A/C'
    ATCT_RAPCON = 'ATCT-RAPCON'
    ATCT_RATCF = 'ATCT-RATCF'
    ATCT_TRACON = 'ATCT-TRACON'
    TRACON = 'TRACON'
    ATCT_TRACAB = 'ATCT-TRACAB'
    ATCT_CERAP = 'ATCT-CERAP'
    STATION_TYPE_CHOICES = (
        (ATCT, 'ATCT'),
        (NON_ATCT, 'NON-ATCT'),
        (ATCT_AC, 'ATCT-A/C'),
        (ATCT_RAPCON, 'ATCT-RAPCON'),
        (ATCT_RATCF, 'ATCT-RATCF'),
        (ATCT_TRACON, 'ATCT-TRACON'),
        (TRACON, 'TRACON'),
        (ATCT_TRACAB, 'ATCT-TRACAB'),
        (ATCT_CERAP, 'ATCT-CERAP'),
    )

    objects = models.GeoManager()

    # Model fields
    station_type = models.CharField(max_length=16, choices=STATION_TYPE_CHOICES, default=NON_ATCT)
    center = models.ForeignKey('Center', blank=True, null=True)
    location = models.PointField()
    city = models.CharField(max_length=64)
    state = models.CharField(blank=True, max_length=2, choices=STATE_CHOICES)
    master = models.ForeignKey('Tower', blank=True, null=True)

    def __str__(self):
        return "%s: %s" % (self.code, self.name)
