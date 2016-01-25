from rest_framework import viewsets
from rest_framework_json_api.mixins import MultipleIDMixin
from airspace import models, serializers

class TowerViewset(MultipleIDMixin, viewsets.ReadOnlyModelViewSet):
    queryset = models.Tower.objects.all()
    serializer_class = serializers.TowerSerializer
