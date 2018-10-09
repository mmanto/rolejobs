# -*- coding: utf-8 -*-

# Importaciones Django
from django.utils.encoding import smart_str
from django.db import models


class Localidad(models.Model):
    departamento = models.ForeignKey('Departamento')
    provincia = models.ForeignKey('Provincia')
    nombre = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = "Localidades"
        ordering = ['nombre']

    def __unicode__(self):
        return smart_str(self.nombre)


class Departamento(models.Model):
    provincia = models.ForeignKey('Provincia')
    nombre = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = "Departamentos"
        ordering = ['nombre']

    def __unicode__(self):
        return smart_str(self.nombre)


class Provincia(models.Model):
    nombre = models.CharField(max_length=100)
    pais = models.ForeignKey('Pais', blank=True, null=True)

    class Meta:
        verbose_name_plural = "Provincias"
        ordering = ['nombre']

    def __unicode__(self):
        return smart_str(self.nombre)


class Pais(models.Model):
    nombre = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = "Paises"
        ordering = ['nombre']

    def __unicode__(self):
        return smart_str(self.nombre)
