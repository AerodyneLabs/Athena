from rest_framework import viewsets
from rest_framework_json_api.mixins import MultipleIDMixin
from airspace import models, serializers

import rest_framework_filters as filters
from django.contrib.gis.geos import Polygon
from rest_framework import exceptions
from django.db.models import Q


class NavaidFilter(filters.FilterSet):
    bounds = filters.MethodFilter()
    search = filters.MethodFilter()

    def filter_bounds(self, name, queryset, value):
        try:
            # Split boundary string into southwest and northeast points
            points = [point.split(',') for point in value.split('|')]
            # Convert strings to floats
            points = [(float(x), float(y)) for x, y in points]
            # Construct bounding box
            bbox = Polygon((
                (points[0][1], points[0][0]),
                (points[0][1], points[1][0]),
                (points[1][1], points[1][0]),
                (points[1][1], points[0][0]),
                (points[0][1], points[0][0]),
            ))
        except ValueError as ve:
            raise exceptions.ParseError(ve)
        except TypeError as te:
            raise exceptions.ParseError(te)
        except ArgumentError as ae:
            raise exceptions.ParseError(ae)

        return queryset.filter(location__within=bbox)

    def filter_search(self, name, queryset, value):
        return queryset.filter(Q(code__iexact=value) | Q(name__icontains=value)).distinct()

    class Meta:
        model = models.Navaid
        fields = ['name']


class NavaidViewset(MultipleIDMixin, viewsets.ReadOnlyModelViewSet):
    queryset = models.Navaid.objects.all()
    serializer_class = serializers.NavaidSerializer
    filter_class = NavaidFilter
