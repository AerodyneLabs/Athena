from django.contrib import admin
from airspace import models

class AirspaceAdmin(admin.ModelAdmin):
    list_filter = ['classification']
    search_fields = ['name']

admin.site.register(models.Airspace, AirspaceAdmin)

class AirspaceBoundaryAdmin(admin.ModelAdmin):
    search_fields = ['name']

admin.site.register(models.AirspaceBoundary, AirspaceBoundaryAdmin)

class CenterAdmin(admin.ModelAdmin):
    search_fields = ['code', 'name', 'city']

admin.site.register(models.Center, CenterAdmin)

class TowerAdmin(admin.ModelAdmin):
    list_filter = ['station_type']
    search_fields = ['code', 'name', 'city']

admin.site.register(models.Tower, TowerAdmin)

class NavaidAdmin(admin.ModelAdmin):
    search_fields = ['code', 'name', 'city']

admin.site.register(models.Navaid, NavaidAdmin)
