from rest_framework import viewsets
from airspace import models, serializers

class AirspaceVolumeViewset(viewsets.ReadOnlyModelViewSet):
    queryset = models.AirspaceVolume.objects.all()
    serializer_class = serializers.AirspaceVolumeSerializer
