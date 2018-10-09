# -*- encoding: utf-8 -*-

# Importaciones Django
from django.contrib import admin

# Importaciones Propias
from .models import Localidad, Departamento, Provincia, Pais


@admin.register(Localidad)
class LocalidadAdmin(admin.ModelAdmin):

    list_display = ['nombre']
    # list_filter = ()
    # search_fields = []


@admin.register(Departamento)
class DepartamentoAdmin(admin.ModelAdmin):

    list_display = ['nombre']
    # list_filter = ()
    # search_fields = []


@admin.register(Provincia)
class ProvinciaAdmin(admin.ModelAdmin):

    list_display = ['nombre']
    # list_filter = ()
    # search_fields = []


@admin.register(Pais)
class PaisAdmin(admin.ModelAdmin):

    list_display = ['nombre']
    # list_filter = ()
    # search_fields = []
