# encoding=utf-8

from __future__ import unicode_literals

from rest_framework import viewsets
from rest_framework.decorators import list_route
from rest_framework.response import Response

from cities_light.models import City, Region, Country

from serializers import CountrySerializer, RegionSerializer, CitySerializer


class CountryViewSet(viewsets.ReadOnlyModelViewSet):
    """Country ViewSet"""

    queryset = Country.objects.all()
    serializer_class = CountrySerializer


class RegionViewSet(viewsets.ReadOnlyModelViewSet):
    """Region ViewSet"""

    serializer_class = RegionSerializer

    def get_queryset(self):
        return Region.objects.all()

    @list_route(methods=("get", ))
    def by_country(self, request, country_pk, *args, **kwargs):
        qs = self.get_queryset().filter(
            country__id=country_pk)

        serializer = RegionSerializer(qs, many=True)
        return Response(serializer.data)


class CityViewSet(viewsets.ReadOnlyModelViewSet):
    """City ViewSet"""

    serializer_class = CitySerializer

    def get_queryset(self):
        return City.objects.all()

    @list_route(methods=("get", ))
    def by_region(self, request, country_pk, region_pk, *args, **kwargs):
        qs = self.get_queryset().filter(
            country_id=country_pk,
            region__id=region_pk)

        serializer = CitySerializer(qs, many=True)
        return Response(serializer.data)
