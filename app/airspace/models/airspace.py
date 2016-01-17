from django.contrib.gis.db import models
from airspace.models import AirspaceBase

class Airspace(AirspaceBase):

    CLASS_A = 'A'
    CLASS_B = 'B'
    CLASS_C = 'C'
    CLASS_D = 'D'
    CLASS_E = 'E'
    CLASS_F = 'F'
    CLASS_G = 'G'
    CLASSIFICATION_CHOICES = (
        (CLASS_A, 'Class A'),
        (CLASS_B, 'Class B'),
        (CLASS_C, 'Class C'),
        (CLASS_D, 'Class D'),
        (CLASS_E, 'Class E'),
        (CLASS_F, 'Class F'),
        (CLASS_G, 'Class G'),
    )

    objects = models.GeoManager()

    # Model fields
    classification = models.CharField(max_length=1, choices=CLASSIFICATION_CHOICES)

    def __str__(self):
        return "%s - Class %s" % (self.name, self.classification)
