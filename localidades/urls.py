# -*- coding: utf-8 -*-

from django.conf.urls import url
from . import views

urlpatterns = [
    url(r"^localidades$", views.localidades_list_view,
        name="localidades"),
    url(r"^localidades/(?P<pk>[0-9]+)/$", views.localidades_detail_view,
        name="localidad"),
#    url(r"^departamentos$", views.DepartamentosViewSet.as_view(),
#        name="departamentos"),
]
