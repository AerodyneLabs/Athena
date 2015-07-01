from django.contrib import admin
from airspace.models.center import Center
from airspace.models.tower import Tower
from airspace.models.navaid import Navaid

admin.site.register(Center)
admin.site.register(Tower)
admin.site.register(Navaid)
