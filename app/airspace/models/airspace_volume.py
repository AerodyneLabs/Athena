from django.contrib.gis.db import models

class AirspaceVolume(models.Model):

    objects = models.GeoManager()

    # Model fields
    name = models.CharField(max_length=64)
    effective = models.DateField()
    parent = models.ForeignKey('AirspaceBase', related_name='volumes')
    low_altitude = models.FloatField()
    low_agl = models.BooleanField(default=False)
    high_altitude = models.FloatField()
    high_agl = models.BooleanField(default=False)
    boundary = models.PolygonField()

    def __str__(self):
        return self.name
