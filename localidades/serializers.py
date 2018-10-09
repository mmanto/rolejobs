# -*- coding: utf-8 -*-

from rest_framework import serializers
from . import models


class LocalidadesSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Localidad


class DepartamentosSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Departamento
