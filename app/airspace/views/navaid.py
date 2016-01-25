from rest_framework import viewsets
from rest_framework_json_api.mixins import MultipleIDMixin
from airspace import models, serializers

class NavaidViewset(MultipleIDMixin, viewsets.ReadOnlyModelViewSet):
    queryset = models.Navaid.objects.all()
    serializer_class = serializers.NavaidSerializer
