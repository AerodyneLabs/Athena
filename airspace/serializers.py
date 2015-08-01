from rest_framework_gis import serializers
from airspace import models

class AirspaceSerializer(serializers.GeoModelSerializer):
    class Meta:
        model = models.Airspace
        fields = ('id', 'name', 'classification')

class AirspaceBoundarySerializer(serializers.GeoModelSerializer):
    class Meta:
        model = models.AirspaceBoundary
        fields = ('id', 'name', 'airspace', 'low_altitude', 'high_altitude', 'boundary')

class CenterSerializer(serializers.GeoModelSerializer):
    class Meta:
        model = models.Center
        fields = ('id', 'code', 'name', 'boundary')

class NavaidSerializer(serializers.GeoModelSerializer):
    class Meta:
        model = models.Navaid
        fields = ('id', 'code', 'name', 'location', 'city', 'state', 'variation', 'service_volume', 'station_type')

class TowerSerializer(serializers.GeoModelSerializer):
    class Meta:
        model = models.Tower
        fields = ('id', 'code', 'name', 'station_type', 'location', 'center', 'city', 'state', 'master')
