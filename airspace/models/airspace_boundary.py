from django.contrib.gis.db import models

class AirspaceBoundary(models.Model):

    objects = models.GeoManager()

    # Model fields
    name = models.CharField(max_length=64)
    effective = models.DateField()
    airspace = models.ForeignKey('Airspace')
    low_altitude = models.FloatField()
    high_altitude = models.FloatField()
    boundary = models.PolygonField()

    def __str__(self):
        return self.name
