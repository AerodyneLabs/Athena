from django.db import models

class ModelRun(models.Model):

    # Model fields
    effective = models.DateTimeField()
    modified = models.DateTimeField()
    spatial_resolution = models.FloatField()
    temporal_resolution = models.DurationField()
    source = models.CharField(max_length=32)

    def __str__(self):
        return "%s-%s (%s / %s deg)" % (self.source, self.effective, self.temporal_resolution, self.spatial_resolution)
