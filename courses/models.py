# encoding: utf-8
from __future__ import unicode_literals

from django.db import models
from django.utils.translation import gettext as _

from cities_light.models import (City, Region, Country)

from accounts.models import User
from utils.helpers import get_company_logo_path

from courses.constants import COURSES_TYPE_CHOICES, CURRENCY_TYPE_CHOICES


class Course(models.Model):

    owner = models.ForeignKey(
        User,
        null=False,
        blank=False,
    )

    title = models.CharField(
        max_length=255,
        null=False,
        blank=False,
        verbose_name=_("Titulo")
    )

    description = models.TextField(verbose_name=_("Descripción"))

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name=_("Precio")
    )

    currency_type = models.IntegerField(
        null=False,
        blank=False,
        choices=CURRENCY_TYPE_CHOICES,
        verbose_name=_("Moneda")
    )

    course_type = models.IntegerField(
        null=False,
        blank=False,
        choices=COURSES_TYPE_CHOICES,
        verbose_name=_("Tipo de curso")
    )

    company_data_from_owner = models.BooleanField(
        default=True,
        verbose_name=_("Datos desde empresa")
    )

    _company = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name=_("Empresa")
    )

    _company_logo = models.FileField(
        upload_to=get_company_logo_path,
        null=True,
        blank=True,
        verbose_name=_("Logo de la empresa")
    )

    notify_by_email = models.BooleanField(
        default=False,
        verbose_name=_("Notificación vía email de interesados")
    )

    address = models.CharField(
        max_length=100,
        blank=True,
        verbose_name=_("Direccion"))

    city = models.ForeignKey(
        City,
        null=True,
        blank=True,
        verbose_name=_("Ciudad"))

    region = models.ForeignKey(
        Region,
        null=True,
        blank=True,
        verbose_name=_("Provincia"))

    country = models.ForeignKey(
        Country,
        null=True,
        blank=True,
        verbose_name=_(u"País"))

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def geodata(self):
        return {
            "country": self.country,
            "region": self.region,
            "city": self.city,
            "address": self.address}

    @property
    def course_type_text(self):
        co = [v for i, v in COURSES_TYPE_CHOICES if i == self.course_type]
        return co[0]

    @property
    def currency_type_text(self):
        co = [v for i, v in CURRENCY_TYPE_CHOICES if i == self.currency_type]
        return co[0]

    @property
    def company(self):
        if self.company_data_from_owner:
            return self.owner.profile.name_company
        return self._company_name

    @company.setter
    def company(self, value):
        if not self.company_data_from_owner:
            self._company = value

    @property
    def company_logo(self):
        if self.company_data_from_owner:
            return self.owner.profile.logo
        return self._company_logo

    @company_logo.setter
    def company_logo(self, value):
        if not self.company_data_from_owner:
            self._company_logo = value


class CoursePostulation(models.Model):

    course = models.ForeignKey(
        Course,
        null=False,
        blank=False,
    )

    user = models.ForeignKey(
        User,
        null=False,
        blank=False,
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    readed_at = models.DateTimeField(null=True, blank=False)

    class Meta:
        unique_together = ("course", "user")
