from rest_framework import viewsets
from airspace import models, serializers

class TowerViewset(viewsets.ReadOnlyModelViewSet):
    queryset = models.Tower.objects.all()
    serializer_class = serializers.TowerSerializer
