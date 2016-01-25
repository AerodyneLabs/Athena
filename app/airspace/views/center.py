from rest_framework import viewsets
from airspace import models, serializers

class CenterViewset(viewsets.ReadOnlyModelViewSet):
    queryset = models.Center.objects.all()
    serializer_class = serializers.CenterSerializer
