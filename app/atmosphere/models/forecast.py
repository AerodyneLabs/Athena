from django.db import models
from atmosphere.models import ModelRun

class Forecast(models.Model):

    # Model fields
    model_run = models.ForeignKey('ModelRun')
    forecast_time = models.DateTimeField()

    def __str__(self):
        return "%s (%s)" % (self.forecast_time, self.model_run.effective)
