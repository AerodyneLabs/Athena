from django.contrib.gis.db import models
from localflavor.us.us_states import STATE_CHOICES

class Center(models.Model):

    objects = models.GeoManager()

    # Model fields
    code = models.CharField(max_length=4)
    name = models.CharField(max_length=64)
    effective = models.DateField()
    boundary = models.MultiPolygonField()
    location = models.PointField()
    city = models.CharField(max_length=64)
    state = models.CharField(blank=True, max_length=2, choices=STATE_CHOICES)

    def __str__(self):
        return "%s: %s" % (self.code, self.name)
