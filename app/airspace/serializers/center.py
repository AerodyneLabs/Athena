from rest_framework import serializers
from rest_framework_gis import serializers as geo_serializers
from airspace import models
from airspace.serializers import AirspaceVolumeSerializer

class CenterSerializer(geo_serializers.GeoModelSerializer):
    volumes = AirspaceVolumeSerializer(many=True, read_only=True)

    class Meta:
        model = models.Center
        fields = ('id', 'code', 'name', 'effective', 'location', 'city', 'state', 'volumes')
