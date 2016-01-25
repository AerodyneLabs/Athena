from rest_framework import viewsets
from rest_framework_json_api.mixins import MultipleIDMixin
from airspace import models, serializers

class AirspaceVolumeViewset(MultipleIDMixin, viewsets.ReadOnlyModelViewSet):
    queryset = models.AirspaceVolume.objects.all()
    serializer_class = serializers.AirspaceVolumeSerializer
