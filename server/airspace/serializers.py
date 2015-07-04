from rest_framework_gis import serializers
from airspace import models

class CenterSerializer(serializers.GeoModelSerializer):
    class Meta:
        model = models.center.Center
        fields = ('id', 'code', 'name', 'boundary')

class NavaidSerializer(serializers.GeoModelSerializer):
    class Meta:
        model = models.navaid.Navaid
        fields = ('id', 'code', 'name', 'location', 'city', 'state', 'variation', 'service_volume', 'station_type')

class TowerSerializer(serializers.GeoModelSerializer):
    class Meta:
        model = models.tower.Tower
        fields = ('id', 'code', 'name', 'location', 'center', 'city', 'state', 'master')
