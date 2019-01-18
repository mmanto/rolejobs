# encoding=utf-8

from __future__ import unicode_literals

from django.db import models
from django.utils.translation import gettext as _
from django.core.exceptions import ValidationError

from utils.models import SimpleItemModel
from accounts.models import User

from cities_light.models import Country

from postulant.choices import COMPLETION_EDUCATION, COMPLETION_LANGUAGES

from education.choices import EDUCATION_GRADES,CERTIFICATIONS



class Institution(models.Model):
    """Education insitution"""

    name = models.CharField(
        max_length=100,
        null=False,
        blank=False,
        verbose_name=_(u"Nombre"))

    description = models.CharField(
        max_length=500,
        null=True,
        blank=True,
        verbose_name=_(u"Descripción"))

    education_levels = models.IntegerField(
        null=False,
        blank=False,
        default=0,
        verbose_name=_(u"Niveles"))

    created_by = models.ForeignKey(
        User,
        null=True,
        blank=True,
        verbose_name=_(u"Creado por")
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def add_level(self, level):
        self.education_levels = self.education_levels | level
        return self.education_levels

    def is_level(self, level):
        return self.education_levels & level

    def list_levels(self):
        return [v for l, v in EDUCATION_GRADES if self.education_levels & l]

    def __unicode__(self):
        return u"%s" % self.name


class EducationArea(models.Model):
    
    name = models.CharField(
        max_length=100,
        verbose_name=_(u'Nombre')
    )

    def __unicode__(self):
        return u"%s" % self.name

    class Meta:
        verbose_name = u'Área de estudio'
        verbose_name_plural = u'Áreas de estudio'

class UserEducation(models.Model):
    """Education model"""

    user = models.ForeignKey(
        User,
        null=False,
        blank=False,
        related_name="education")

    level = models.IntegerField(
        null=False,
        blank=False,
        choices=EDUCATION_GRADES,
        verbose_name=_(u"Nivél de educación"))

    institution = models.ForeignKey(
        Institution,
        null=False,
        blank=False,
        verbose_name=_(u"Institución"))


    career = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        verbose_name=_(u"Carrera")
    )

    country = models.ForeignKey(
        Country,
        null=False,
        blank=False,
        verbose_name=_(u"País"),
        default=None)

    education_area = models.ForeignKey(
        EducationArea,
        null=False,
        blank=False,
        verbose_name=_(u"Área de estudios"),
        default=None)

    comments = models.TextField(

        null=True,
        blank=True,
        verbose_name=_(u'Comentarios')
    )

    

    start_date = models.DateField(
        null=False,
        blank=False,
        verbose_name=_(u"Fecha de inicio"))

    end_date = models.DateField(
        null=True,
        blank=True,
        default=None,
        verbose_name=_(u"Fecha de finalización"))

    is_current = models.BooleanField(
        null=False,
        blank=False,
        default=False,
        verbose_name=_(u"Cursando actualmente"))

    finished = models.BooleanField(
        null=False,
        blank=False,
        default=False,
        verbose_name=_(u"Terminado"))

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def level_text(self):
        label = [l for v, l in EDUCATION_GRADES if v == self.level]
        if len(label):
            return label[0]
        else:
            return None

    def save(self, *args, **kwargs):
        self.user.set_complete(COMPLETION_EDUCATION)
        super(UserEducation, self).save(*args, **kwargs)


class UserCertification(models.Model):
    """User certifications"""

    education = models.ForeignKey(
        UserEducation,
        null=False,
        related_name="certifications",
        verbose_name=_(u"Adquirido en"))

    type = models.PositiveSmallIntegerField(
        null=False,
        blank=False,
        choices=CERTIFICATIONS,
        verbose_name=_("Tipo"))

    name = models.CharField(
        max_length=100,
        null=False,
        blank=False,
        verbose_name=_(u"Nombre"))

    description = models.CharField(
        max_length=600,
        null=True,
        blank=True,
        verbose_name=_("Descripción"))

    number_certification = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        verbose_name=_('Número Certificado'))

    number_examen = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        verbose_name=_('Número de Examen'))

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def type_text(self):
        label = [l for v, l in CERTIFICATIONS if v == self.type]
        if len(label):
            return label[0]
        else:
            return None


class Language(SimpleItemModel):
    """Languages"""
    pass

class Computerknowledge(SimpleItemModel):
    """Computerknowledges"""
    pass


class UserLanguages(models.Model):
    """Languages of users"""

    user = models.ForeignKey(
        User,
        null=False,
        blank=False,
        related_name="languages")

    language = models.ForeignKey(
        Language,
        null=False,
        blank=False,
        verbose_name=_(u"Lenguaje"))

    level = models.IntegerField(
        null=False,
        blank=False,
        verbose_name=_(u"Nivél"))

    @property
    def name(self):
        return u"%s" % self.language.name

    def clean(self):

        if self.level < 0 or self.level > 10:
            raise ValidationError(_(u"El nivél debe ser un número entre " +
                                    u"1 y 10"))

    def save(self, *args, **kwargs):
        self.user.set_complete(COMPLETION_LANGUAGES)
        super(UserLanguages, self).save(*args, **kwargs)

    def __unicode__(self):
        return u"%s" % self.name

class UserComputerknowledge(models.Model):
    """Computerknowledges of users"""

    user = models.ForeignKey(
        User,
        null=False,
        blank=False,
        related_name="computerknowledges")

    computerknowledge = models.ForeignKey(
        Computerknowledge,
        null=False,
        blank=False,
        verbose_name=_(u"Conocimiento Informático"))

    level = models.IntegerField(
        null=False,
        blank=False,
        verbose_name=_(u"Nivél"))

    @property
    def name(self):
        return u"%s" % self.computerknowledge.name

    def clean(self):

        if self.level < 0 or self.level > 10:
            raise ValidationError(_(u"El nivél debe ser un número entre " +
                                    u"1 y 10"))

    def save(self, *args, **kwargs):
        self.user.set_complete(COMPLETION_LANGUAGES)
        super(UserComputerknowledge, self).save(*args, **kwargs)

    def __unicode__(self):
        return u"%s" % self.name
