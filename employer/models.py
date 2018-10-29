# encoding=utf-8

from __future__ import unicode_literals

from django.core.validators import RegexValidator
from django.utils.translation import gettext as _
from django.core.exceptions import ObjectDoesNotExist
from django.db import models

from taggit.managers import TaggableManager

from accounts.models import Profile, User

TYPE_REFERENCE = (
    ("A", _("Google ")), ("B", _("Envio de Email")),
    ("C", _("Facebook")), ("C", _("Otros"))
)

PHONE_REGEX = RegexValidator(
    regex=r'^\+?1?\d{9,15}$',
    message=_("El número de teléfono debe tener el formato: "
              "'+999999999'. Hasta 15 dígitos permitidos.")
)

TYPE_COMPANY = (
    (None, _("Seleccione un elemento")),
    ("A", _("Empleador Directo")),
    ("B", _("Agencia de Reclutamiento")),
    ("C", _("Servicios Temporales"))
)

SECTOR_EMPRESARIAL = (
    (None, _("Sector empresarial")),
    ("A", _("Informática")),
    ("B", _("Metalurgia")),
    ("C", _("Agro"))
)

CVREQUEST_NEW = 0x00
CVREQUEST_ACCEPTED = 0x10
CVREQUEST_REJECTED = 0x20

CVREQUESTS_CHOICES = (
    (CVREQUEST_NEW, _(u"Nueva")),
    (CVREQUEST_ACCEPTED, _(u"Aceptada")),
    (CVREQUEST_REJECTED, _(u"Rechazada")),
)


class Employer(Profile):
    """Employer model"""

    name_company = models.CharField(
        max_length=100,
        null=False,
        blank=False,
        verbose_name=_("Nombre de la Empresa"))

    razon_social = models.CharField(
        max_length=100, verbose_name=_("Razon Social"))
    responsability_iva = models.CharField(
        max_length=100, verbose_name=_("Responsabilidad ante el IVA"))
    sector_empresarial = models.CharField(
        max_length=100, blank=True, verbose_name=_("Sector empresarial"))
    workforce = models.IntegerField(default=0,
                                    verbose_name=_("Numero de Trabajadores"))
    tipology = models.CharField(
                                max_length=100, choices=TYPE_COMPANY,
                                verbose_name=_("Tipo de Empresa"))
    description = models.TextField(
        blank=True, null=True, verbose_name=_("Descripcion de la Empresa"))
    website = models.CharField(max_length=100, verbose_name=_("Sitio Web"))
    cuit = models.CharField(max_length=255, verbose_name=_(
        "CUIT"), null=True, blank=True)
    # @TODO Validate logo
    # logo = models.FileField(upload_to='media', blank=True, null=True,
    #                        verbose_name=_("Logo de la Empresa"),
    #                        validators=[])
    reference = models.CharField(
        max_length=100, choices=TYPE_REFERENCE, verbose_name=_("Referencia"))

    newsletter = models.BooleanField(default=False, verbose_name=_("Noticias"))

    cv_spontany = models.BooleanField(
        default=False, verbose_name=_("CV espontaneos"))

    position = models.CharField(max_length=100, verbose_name=_("Cargo"))

    post_points = models.IntegerField(
        null=False,
        blank=False,
        default=30,
        verbose_name=_(u"Puntos de publicación"))

    @property
    def avatars_object(self):
        return self.user.avatars

    @property
    def avatars(self):
        default = None
        brand = None

        try:
            default = self.avatars_object.get(label="default")
        except ObjectDoesNotExist:
            pass

        try:
            brand = self.avatars_object.get(label="brand")
        except ObjectDoesNotExist:
            pass

        return {
            "default": default.url if default is not None else "",
            "brand": brand.url if brand is not None else ""
        }

    @property
    def is_employer(self):
        return True

    def use_post_points(self, cant):
        self.post_points = self.post_points - cant
        return self.save()

    class Meta:
        verbose_name_plural = "Employers"

    def __unicode__(self):
        return u"%s" % (self.name_company)


class CVRequest(models.Model):

    user = models.ForeignKey(
        User,
        null=False,
        blank=False,
        related_name="cv_request_postulant",
        verbose_name=_(u"Postulante"))

    employer = models.ForeignKey(
        Employer,
        null=False,
        blank=False,
        related_name="cv_request_employer",
        verbose_name=_(u"Empleador"))

    status = models.PositiveSmallIntegerField(
        null=False,
        blank=False,
        default=CVREQUEST_NEW,
        choices=CVREQUESTS_CHOICES,
        verbose_name=_(u"Estado"))

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    readed_at = models.DateTimeField(null=True, blank=True)

    @property
    def status_text(self):
        co = [v for i, v in CVREQUESTS_CHOICES if i == self.status]
        return co[0]

    def set_status(self, status):
        if status not in [i for i, v in CVREQUESTS_CHOICES]:
            raise Exception("Unknow status")

        if status == CVREQUEST_NEW:
            raise Exception("Status can't return to new")

        if not status == self.status:
            self.status = status
            self.save()


class CVTags(models.Model):

    employer = models.ForeignKey(
        Employer,
        null=False,
        blank=False,
        verbose_name=_(u"Empleador"))

    user = models.ForeignKey(
        User,
        null=False,
        blank=False,
        verbose_name=_(u"Postulante"))

    tags = TaggableManager()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('employer', 'user')
