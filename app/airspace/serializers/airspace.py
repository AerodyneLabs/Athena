from rest_framework import serializers
from rest_framework_gis import serializers as geo_serializers
from airspace import models
from airspace.serializers import AirspaceVolumeSerializer

class AirspaceSerializer(geo_serializers.GeoModelSerializer):
    volumes = AirspaceVolumeSerializer(many=True, read_only=True)

    class Meta:
        model = models.Airspace
        fields = ('id', 'name', 'effective', 'classification', 'volumes')
