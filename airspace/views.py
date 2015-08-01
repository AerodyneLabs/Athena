from django.shortcuts import render
from rest_framework import viewsets
from airspace import models, serializers

class AirspaceViewset(viewsets.ReadOnlyModelViewSet):
    queryset = models.Airspace.objects.all()
    serializer_class = serializers.AirspaceSerializer

class AirspaceBoundaryViewset(viewsets.ReadOnlyModelViewSet):
    queryset = models.AirspaceBoundary.objects.all()
    serializer_class = serializers.AirspaceBoundarySerializer

class CenterViewset(viewsets.ReadOnlyModelViewSet):
    queryset = models.Center.objects.all()
    serializer_class = serializers.CenterSerializer
    lookup_field = 'code'

class NavaidViewset(viewsets.ReadOnlyModelViewSet):
    queryset = models.Navaid.objects.all()
    serializer_class = serializers.NavaidSerializer
    lookup_field = 'code'

class TowerViewset(viewsets.ReadOnlyModelViewSet):
    queryset = models.Tower.objects.all()
    serializer_class = serializers.TowerSerializer
    lookup_field = 'code'
