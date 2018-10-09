# -*- coding: utf8 -*-

from __future__ import unicode_literals
import logging

# from django.views.decorators.csrf import csrf_exempt

# from rest_framework import mixins, generics, status
# from rest_framework.decorators import api_view
# from rest_framework.response import Response
from rest_framework import viewsets

from . import models
from . import serializers

logger = logging.getLogger(__name__)


class LocalidadesViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Localidades
    """

    queryset = models.Localidad.objects.all()
    serializer_class = serializers.LocalidadesSerializer


class DepartamentosViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Departamentos
    """

    queryset = models.Departamento.objects.all()
    serializer_class = serializers.DepartamentosSerializer


localidades_list_view = LocalidadesViewSet.as_view({
    'get': 'list'
})

localidades_detail_view = LocalidadesViewSet.as_view({
    'get': 'retrieve'
})
