# encoding=utf-8

from django.conf.urls import url
from views import CountryViewSet, RegionViewSet, CityViewSet

urlpatterns = [
    url(
        r"^countries/?$",
        CountryViewSet.as_view({
            "get": "list"
        })
    ),
    url(
        r"^countries/(?P<pk>[0-9]+)/?$",
        CountryViewSet.as_view({
            "get": "retrieve",
        })
    ),
    url(
        r"^countries/(?P<country_pk>[0-9]+)/regions/?$",
        RegionViewSet.as_view({
            "get": "by_country"
        })
    ),
    url(
        r"^countries/(?P<country_pk>[0-9]+)/regions/(?P<pk>[0-9]+)/?$",
        RegionViewSet.as_view({
            "get": "retrieve"
        })
    ),
    url(
        r"^countries/(?P<country_pk>[0-9]+)/regions/(?P<region_pk>[0-9]+)/cities/?$",
        CityViewSet.as_view({
            "get": "by_region"
        })
    ),
    url(
        r"^countries/(?P<country_pk>[0-9]+)/regions/(?P<region_pk>[0-9]+)/cities/(?P<pk>[0-9]+)/?$",
        CityViewSet.as_view({
            "get": "retrieve"
        })
    ),
]
