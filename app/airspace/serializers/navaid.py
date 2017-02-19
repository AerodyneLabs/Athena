from rest_framework import serializers
from rest_framework_gis import serializers as geo_serializers
from airspace import models
from airspace.serializers import AirspaceVolumeSerializer

class NavaidSerializer(geo_serializers.GeoModelSerializer):
    class Meta:
        model = models.Navaid
        fields = ('id', 'code', 'name', 'effective', 'location', 'city', 'state', 'variation', 'service_volume', 'station_type')
