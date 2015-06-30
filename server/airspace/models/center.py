from django.contrib.gis.db import models

class Center(models.Model):

    objects = models.GeoManager()

    # Model fields
    code = models.CharField(max_length=4)
    name = models.CharField(max_length=64)
    effective = models.DateField()
    boundary = models.MultiPolygonField()

    def __str__(self):
        return "%s: %s" % (self.code, self.name)
