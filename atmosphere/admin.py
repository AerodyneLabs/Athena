from django.contrib import admin
from atmosphere import models

class ModelRunAdmin(admin.ModelAdmin):
    list_filter = ['spatial_resolution', 'temporal_resolution', 'source']
    search_fields = ['effective', 'source']

admin.site.register(models.ModelRun, ModelRunAdmin)

class ForecastAdmin(admin.ModelAdmin):
    list_filter = ['model_run']
    search_fields = ['forecast_time']

admin.site.register(models.Forecast, ForecastAdmin)

class ForecastPointAdmin(admin.ModelAdmin):
    list_filter = ['forecast']
    search_fields = ['location', 'pressure']

admin.site.register(models.ForecastPoint, ForecastPointAdmin)
