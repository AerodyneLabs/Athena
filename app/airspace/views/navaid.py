from rest_framework import viewsets
from airspace import models, serializers

class NavaidViewset(viewsets.ReadOnlyModelViewSet):
    queryset = models.Navaid.objects.all()
    serializer_class = serializers.NavaidSerializer
