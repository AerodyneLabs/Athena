from rest_framework import viewsets
from rest_framework_json_api.mixins import MultipleIDMixin
from airspace import models, serializers

class CenterViewset(MultipleIDMixin, viewsets.ReadOnlyModelViewSet):
    queryset = models.Center.objects.all()
    serializer_class = serializers.CenterSerializer
