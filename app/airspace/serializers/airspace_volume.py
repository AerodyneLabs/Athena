from rest_framework import serializers
from rest_framework_gis import serializers as geo_serializers
from airspace import models

class AirspaceVolumeSerializer(geo_serializers.GeoModelSerializer):
    class Meta:
        model = models.AirspaceVolume
        fields = ('id', 'name', 'low_altitude', 'high_altitude', 'boundary', 'low_agl', 'high_agl', 'effective')
