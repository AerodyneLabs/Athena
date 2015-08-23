from django.contrib.gis.db import models

class ForecastPoint(models.Model):

    # Model fields
    forecast = models.ForeignKey('Forecast')
    location = models.PointField(dim=3)
    pressure = models.FloatField()
    temperature = models.FloatField()
    humidity = models.FloatField()
    wind_u = models.FloatField()
    wind_v = models.FloatField()

    def __str__(self):
        return "%s (%s, %s) %sPa" % (self.forecast.forecast_time, self.location.y, self.location.x, self.pressure)
