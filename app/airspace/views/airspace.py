from rest_framework import viewsets
from airspace import models, serializers

class AirspaceViewset(viewsets.ReadOnlyModelViewSet):
    queryset = models.Airspace.objects.all()
    serializer_class = serializers.AirspaceSerializer
