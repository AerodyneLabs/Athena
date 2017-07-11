from django.contrib import admin
from airspace import models

class AirspaceBaseAdmin(admin.ModelAdmin):
    search_fields = ['name']

admin.site.register(models.AirspaceBase, AirspaceBaseAdmin)

class AirspaceVolumeAdmin(admin.ModelAdmin):
    search_fields = ['name']

admin.site.register(models.AirspaceVolume, AirspaceVolumeAdmin)

class AirspaceVolumeInline(admin.TabularInline):
    model = models.AirspaceVolume
    extra = 0

class AirspaceAdmin(admin.ModelAdmin):
    search_fields = ['name']
    list_filter = ['classification']
    list_display = ['name', 'classification', 'effective']
    inlines = [AirspaceVolumeInline]

admin.site.register(models.Airspace, AirspaceAdmin)

class CenterAdmin(admin.ModelAdmin):
    search_fields = ['code', 'name', 'city']
    list_filter = ['effective']
    list_display = ['code', 'name', 'city', 'state', 'effective']
    inlines = [AirspaceVolumeInline]

admin.site.register(models.Center, CenterAdmin)

class TowerAdmin(admin.ModelAdmin):
    search_fields = ['code', 'name', 'city']
    list_filter = ['station_type', 'artcc', 'effective']
    list_display = ['code', 'name', 'station_type', 'center', 'city', 'state', 'effective']

admin.site.register(models.Tower, TowerAdmin)

class NavaidAdmin(admin.ModelAdmin):
    search_fields = ['code', 'name', 'city']
    list_filter = ['station_type', 'service_volume', 'effective']
    list_display = ['code', 'name', 'station_type', 'service_volume', 'city', 'state', 'effective']

admin.site.register(models.Navaid, NavaidAdmin)
