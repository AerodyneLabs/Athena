from django.contrib.gis.db import models
from localflavor.us.us_states import STATE_CHOICES

class Navaid(models.Model):

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
    code = models.CharField(max_length=4)
    name = models.CharField(max_length=64)
    effective = models.DateField()
    location = models.PointField()
    city = models.CharField(max_length=64)
    state = models.CharField(blank=True, max_length=2, choices=STATE_CHOICES)
    variation = models.FloatField()
    service_volume = models.CharField(max_length=1, choices=SERVICE_VOLUME_CHOICES)
    station_type = models.CharField(max_length=16, choices=STATION_TYPE_CHOICES)

    def __str__(self):
        return "%s: %s" % (self.code, self.name)
