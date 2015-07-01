from django.contrib import admin
from airspace.models.center import Center
from airspace.models.tower import Tower

admin.site.register(Center)
admin.site.register(Tower)
