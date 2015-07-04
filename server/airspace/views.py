from django.shortcuts import render
from rest_framework import viewsets
from airspace import models, serializers

class CenterViewset(viewsets.ReadOnlyModelViewSet):
    queryset = models.center.Center.objects.all()
    serializer_class = serializers.CenterSerializer
    lookup_field = 'code'

class NavaidViewset(viewsets.ReadOnlyModelViewSet):
    queryset = models.navaid.Navaid.objects.all()
    serializer_class = serializers.NavaidSerializer
    lookup_field = 'code'

class TowerViewset(viewsets.ReadOnlyModelViewSet):
    queryset = models.tower.Tower.objects.all()
    serializer_class = serializers.TowerSerializer
    lookup_field = 'code'
