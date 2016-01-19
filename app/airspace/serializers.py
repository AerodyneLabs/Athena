from rest_framework import serializers
from rest_framework_gis import serializers as geo_serializers
from airspace import models

class AirspaceVolumeSerializer(geo_serializers.GeoModelSerializer):
    class Meta:
        model = models.AirspaceVolume
        fields = ('id', 'name', 'low_altitude', 'high_altitude', 'boundary', 'low_agl', 'high_agl', 'effective')

class AirspaceSerializer(geo_serializers.GeoModelSerializer):
    volumes = AirspaceVolumeSerializer(many=True, read_only=True)

    class Meta:
        model = models.Airspace
        fields = ('id', 'name', 'effective', 'classification', 'volumes')

class CenterSerializer(geo_serializers.GeoModelSerializer):
    volumes = AirspaceVolumeSerializer(many=True, read_only=True)

    class Meta:
        model = models.Center
        fields = ('id', 'code', 'name', 'effective', 'location', 'city', 'state', 'volumes')

class NavaidSerializer(geo_serializers.GeoModelSerializer):
    class Meta:
        model = models.Navaid
        fields = ('id', 'code', 'name', 'effective', 'location', 'city', 'state', 'variation', 'service_volume', 'station_type')

class TowerSerializer(geo_serializers.GeoModelSerializer):
    class Meta:
        model = models.Tower
        fields = ('id', 'code', 'name', 'station_type', 'effective', 'location', 'center', 'city', 'state', 'master')
