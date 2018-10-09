# encoding=utf-8

from __future__ import unicode_literals
from collections import namedtuple

from rest_framework import serializers
from cities_light.models import (City, Region, Country)

GeoTuple = namedtuple("GeoTuple", "country region city address")


class CountrySerializer(serializers.ModelSerializer):
    """Country serializer"""

    class Meta:
        model = Country
        exclude = (
            "alternate_names",
            "name_ascii")


class CountryShortSerializer(serializers.ModelSerializer):
    """Shorter serializer for country"""

    class Meta:
        model = Country
        fields = ("id", "name", "tld")


class RegionSerializer(serializers.ModelSerializer):
    """Region serializer"""

    class Meta:
        model = Region
        exclude = (
            "alternate_names",
            "name_ascii",
            "country")


class RegionShortSerializer(serializers.ModelSerializer):
    """Shorter serializer for region"""

    class Meta:
        model = Region
        fields = ("id", "name", "display_name")


class CitySerializer(serializers.ModelSerializer):
    """Cities serializer"""

    class Meta:
        model = City
        exclude = (
            "alternate_names",
            "name_ascii",
            "country",
            "region")


class CityShortSerializer(serializers.ModelSerializer):
    """Shorter serializer for city"""

    class Meta:
        model = City
        fields = ("id", "name", "display_name")


class GeoDataSerializer(serializers.Serializer):
    """Serialzier for geo data"""

    address = serializers.CharField(
        read_only=True,
        max_length=200)

    country = CountryShortSerializer(
        read_only=True)

    region = RegionShortSerializer(
        read_only=True)

    city = CityShortSerializer(
        read_only=True)

    display_name = serializers.SerializerMethodField(
        read_only=True)

    def get_display_name(self, obj):
        geoname = ""

        if type(obj) is dict:
            obj = GeoTuple(**obj)

        if obj.city is not None:
            geoname = obj.city.display_name
        elif obj.region is not None:
            geoname = obj.region.display_name
        elif obj.country is not None:
            geoname = obj.country.name
        else:
            geoname = ""

        if obj.address is not None:
            geoname = u"%s, %s" % (obj.address, geoname)

        return geoname
