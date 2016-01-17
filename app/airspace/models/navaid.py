from django.contrib.gis.db import models
from localflavor.us.us_states import STATE_CHOICES
from airspace.models import AirspaceBase

class Navaid(AirspaceBase):

    # Constants
    LOW_VOLUME = 'L'
    HIGH_VOLUME = 'H'
    TERMINAL_VOLUME = 'T'
    SERVICE_VOLUME_CHOICES = (
        (LOW_VOLUME, 'Low'),
        (HIGH_VOLUME, 'High'),
        (TERMINAL_VOLUME, 'Terminal'),
    )

    VOR = 'VOR'
    DME = 'DME'
    VOR_DME = 'VOR/DME'
    VORTAC = 'VORTAC'
    TACAN = 'TACAN'
    STATION_TYPE_CHOICES = (
        (VOR, 'VOR'),
        (DME, 'DME'),
        (VOR_DME, 'VOR/DME'),
        (VORTAC, 'VORTAC'),
        (TACAN, 'TACAN'),
    )

    objects = models.GeoManager()

    # Model fields
    location = models.PointField(dim=3)
    city = models.CharField(max_length=64)
    state = models.CharField(blank=True, max_length=2, choices=STATE_CHOICES)
    variation = models.FloatField()
    service_volume = models.CharField(max_length=1, choices=SERVICE_VOLUME_CHOICES)
    station_type = models.CharField(max_length=16, choices=STATION_TYPE_CHOICES)

    def __str__(self):
        return "%s: %s" % (self.code, self.name)
