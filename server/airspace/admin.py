from django.contrib import admin
from airspace.models.center import Center
from airspace.models.tower import Tower
from airspace.models.navaid import Navaid


class CenterAdmin(admin.ModelAdmin):
    search_fields = ['code', 'name', 'city']

admin.site.register(Center, CenterAdmin)

class TowerAdmin(admin.ModelAdmin):
    list_filter = ['station_type']
    search_fields = ['code', 'name', 'city']

admin.site.register(Tower, TowerAdmin)

class NavaidAdmin(admin.ModelAdmin):
    search_fields = ['code', 'name', 'city']

admin.site.register(Navaid, NavaidAdmin)
