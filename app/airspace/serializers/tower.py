from rest_framework import serializers
from rest_framework_gis import serializers as geo_serializers
from airspace import models

class TowerSerializer(geo_serializers.GeoModelSerializer):
    class Meta:
        model = models.Tower
        fields = ('id', 'code', 'name', 'station_type', 'effective', 'location', 'center', 'city', 'state', 'master')
