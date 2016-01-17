from django.shortcuts import render
from rest_framework import viewsets
from airspace import models, serializers

class AirspaceViewset(viewsets.ReadOnlyModelViewSet):
    queryset = models.Airspace.objects.all()
    serializer_class = serializers.AirspaceSerializer

class AirspaceVolumeViewset(viewsets.ReadOnlyModelViewSet):
    queryset = models.AirspaceVolume.objects.all()
    serializer_class = serializers.AirspaceVolumeSerializer

class CenterViewset(viewsets.ReadOnlyModelViewSet):
    queryset = models.Center.objects.all()
    serializer_class = serializers.CenterSerializer

class NavaidViewset(viewsets.ReadOnlyModelViewSet):
    queryset = models.Navaid.objects.all()
    serializer_class = serializers.NavaidSerializer

class TowerViewset(viewsets.ReadOnlyModelViewSet):
    queryset = models.Tower.objects.all()
    serializer_class = serializers.TowerSerializer
