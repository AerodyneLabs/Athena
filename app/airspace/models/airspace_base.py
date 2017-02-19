from django.db import models

class AirspaceBase(models.Model):
    code = models.CharField(max_length=10)
    name = models.CharField(max_length=64)
    effective = models.DateField()

    def __str__(self):
        return "%s: %s" % (self.code, self.name)
