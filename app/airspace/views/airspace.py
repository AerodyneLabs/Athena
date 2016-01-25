from rest_framework import viewsets
from rest_framework_json_api.mixins import MultipleIDMixin
from airspace import models, serializers

class AirspaceViewset(MultipleIDMixin, viewsets.ReadOnlyModelViewSet):
    queryset = models.Airspace.objects.all()
    serializer_class = serializers.AirspaceSerializer
