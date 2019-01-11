# encoding=utf-8

from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext as _
from rolejobs_api.media import resolve_media_url

from cities_light.models import (
    Country,
)

# from utils.validates import validate_file_extension, validate_size
# from utils.views import check_model_complete

from jobs.models import (
    Area,
    SubArea,
    TitleRole,
    Position,
    Hierarchy,
    BranchActivity,
    Role,
)

from accounts.models import User
from accounts.models import Profile

from postulant.helpers import get_attachcv_directory
from postulant.choices import (
    MARRIED_STATUS,
    TYPE_LICENCE,
    YES_NO_CHOICES,
    CV_COMPLETION,
    COMPLETION_PROFILE,
    COMPLETION_BIO,
    COMPLETION_EXPERIENCES,
    COMPLETION_REFERENCES,
    STAFF_CHARGE,
    CURRENCY_CHOICES,
    REFERENCE_TYPES,
)


class Postulant(Profile):
    """Postulant model"""

    category = models.CharField(
        max_length=100,
        verbose_name=_("Categoría"))

    complete = models.IntegerField(default=0)

    # photo = models.FileField(upload_to='profiles', blank=True, null=True)

    marital_status = models.IntegerField(
        choices=MARRIED_STATUS,
        verbose_name=_('Estado Civil'))

    dni = models.IntegerField(
        null=False,
        blank=False,
        verbose_name=_('DNI'))

    date_of_birth = models.DateField(
        null=False,
        blank=False,
        verbose_name=_('Fecha de nacimiento'))

    country_of_birth = models.ForeignKey(
        Country,
        null=False,
        verbose_name=_("Nacionalidad"))

    postal_code = models.CharField(
        max_length=20,
        null=False,
        blank=False,
        verbose_name=_('Código Postal'))

    driver_license = models.IntegerField(
        null=True,
        choices=TYPE_LICENCE,
        verbose_name=_('Licencia de conducir'))

    own_vehicle = models.BooleanField(
        null=False,
        default=False,
        choices=YES_NO_CHOICES,
        verbose_name=_('¿Posée vehículo propio?'))

    has_disability = models.BooleanField(
        null=False,
        default=False,
        verbose_name=_('¿Posee algún tipo de discapacidad?'))

    @property
    def is_postulant(self):
        return True

    @property
    def last_update(self):
        return self.user.last_profile_update

    @property
    def completed(self):
        return self.user.calculate_complete(CV_COMPLETION)

    @property
    def biographic(self):
        return self.user.biographic

    @property
    def experience(self):
        return self.user.experience

    @property
    def roles(self):
        return self.user.postulant_roles

    @property
    def education(self):
        return self.user.education

    @property
    def languages(self):
        return self.user.languages

    @property
    def max_education(self):
        max_education = self.education.all().aggregate(models.Max("level"))
        return max_education["level__max"]

    @property
    def education_level(self):
        levels = [e.level for e in self.education.all()]
        level = 0
        for l in levels:
            level |= l
        return level

    @property
    def education_finish_level(self):
        levels = [e.level for e in self.education.filter(finished=True)]
        level = 0
        for l in levels:
            level |= l
        return level

    @property
    def completed_info(self):
        completed = self.user.calculate_complete(CV_COMPLETION)

        items = [{
            "value": k,
            "name": v,
            "is_completed": self.user.has_completed(k)
        } for k, v in CV_COMPLETION]

        return {
            "completed": completed,
            "items": items}

    def save(self, *args, **kwargs):
        self.user.set_complete(COMPLETION_PROFILE)
        super(Postulant, self).save(*args, **kwargs)

    def __unicode__(self):
        return "%s %s" % (self.first_name, self.last_name)


class Biographic(models.Model):

    user = models.OneToOneField(
        User,
        related_name='biographic')

    description = models.TextField(
        max_length=600,
        blank=False,
        null=False,
        verbose_name=_(
            'Escribe una breve presentación sobre tu experiencia laboral...')
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return u"%s" % self.description

    def save(self, *args, **kwargs):
        self.user.set_complete(COMPLETION_BIO)
        super(Biographic, self).save(*args, **kwargs)


class ProfessionalExperience(models.Model):
    """Porfessional experience of postualant"""

    user = models.ForeignKey(
        User,
        null=False,
        blank=False,
        related_name='experience')

    company_name = models.CharField(
        max_length=100,
        null=False,
        blank=False,
        verbose_name=_("Empresa"))

    company_address = models.CharField(
        max_length=100,
        null=False,
        blank=False,
        verbose_name=_("Dirección"))

    title = models.ForeignKey(
        TitleRole,
        null=False,
        blank=False,
        verbose_name=_('Titulo'))

    position = models.ForeignKey(
        Position,
        null=False,
        blank=False,
        verbose_name=_('Puesto'))

    hierarchy = models.ForeignKey(
        Hierarchy,
        null=False,
        blank=False,
        verbose_name=_('Jerarquia'))

    area = models.ForeignKey(
        Area,
        null=False,
        blank=False,
        verbose_name=_('Area'))

    subarea = models.ForeignKey(
        SubArea,
        null=False,
        blank=False,
        verbose_name=_('Subárea'))

#     role = models.ForeignKey(
#         Role,
#         null=False,
#         blank=False,
#         verbose_name=_('Roles'))

    branch_activity = models.ForeignKey(
        BranchActivity,
        null=False,
        blank=False,
        verbose_name=_('Ramo o actividad'))

    start_date = models.DateField(
        null=False,
        blank=False,
        verbose_name=_('Fecha de inicio'))

    end_date = models.DateField(
        null=True,
        blank=True,
        verbose_name=_('Fecha de finalización'))

    is_current = models.BooleanField(
        null=False,
        blank=False,
        default=False,
        verbose_name=_("Al presente"))

    description = models.TextField(
        blank=True,
        null=True,
        verbose_name=_('Descripción de responsabilidades y logros'))

    staff_charge = models.IntegerField(
        null=True,
        blank=True,
        choices=STAFF_CHARGE,
        verbose_name=_('Personal a cargo'))

    budget = models.BooleanField(
        null=False,
        blank=False,
        default=False,
        choices=YES_NO_CHOICES,
        verbose_name=_('Presupuesto anual propio'))

    currency = models.CharField(
        max_length=5,
        null=False,
        blank=False,
        choices=CURRENCY_CHOICES,
        verbose_name=_('Moneda'))

    salary = models.FloatField(
        null=False,
        blank=False,
        verbose_name=_('Sueldo'))

    show_salary = models.BooleanField(
        null=False,
        blank=False,
        default=False,
        verbose_name=_('Mostrar Sueldo'))

#    with_experience = models.BooleanField(
#        null=False,
#        blank=False,
#        default=False,
#        verbose_name=_('No tengo ninguna experiencia'))

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self):

        # Validate if is currently, dont has end date
        if self.is_current and self.end_date is not None:
            raise ValidationError(_("Si el puesto es actual, no puede tener" +
                                    " fecha de finalización"))

        # Validate if end date is bigger that start date
        if self.end_data and self.start_date > self.end_date:
            raise ValidationError(_("La decha de inicio no puede ser mayor" +
                                    " a la fecha de finalización"))

    def save(self, *args, **kwargs):
        self.user.set_complete(COMPLETION_EXPERIENCES)
        super(ProfessionalExperience, self).save(*args, **kwargs)


class ProfessionalReference(models.Model):
    """Profesional reference"""

    experience = models.ForeignKey(
        ProfessionalExperience,
        null=False,
        blank=False,
        related_name="references")

    name = models.CharField(
        max_length=100,
        null=False,
        blank=False,
        verbose_name=_(u"Nombre"))

    email = models.EmailField(
        null=True,
        blank=True,
        verbose_name=_(u"Direccion de correo electrónico"))

    phone = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        verbose_name=_(u"Teléfono de contacto"))

    type = models.IntegerField(
        null=False,
        blank=False,
        choices=REFERENCE_TYPES,
        verbose_name=_(u"Relación laboral"))

    # @TODO Confirm references by email
    confirmed = models.BooleanField(
        null=False,
        blank=False,
        default=False)

    created_by = models.ForeignKey(
        User,
        null=False,
        blank=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def type_text(self):
        label = [l for v, l in REFERENCE_TYPES if v == self.type]
        if len(label):
            return label[0]
        else:
            return None

    def save(self, *args, **kwargs):
        self.experience.user.set_complete(COMPLETION_REFERENCES)
        super(ProfessionalReference, self).save(*args, **kwargs)

    def __unicode__(self):
        return u"%s" % self.name


class PostulantRoles(models.Model):
    """Postulant roles"""

    user = models.OneToOneField(
        User,
        null=False,
        blank=False,
        related_name='postulant_roles')

    roles = models.ManyToManyField(
        Role,
        verbose_name=_(u"Roles"))

    def set_roles(self, roles_pks):
        roles_pks = [int(pk) for pk in roles_pks]
        roles = [Role.objects.get(id=pk) for pk in roles_pks]
        self.roles.set(roles)

    @classmethod
    def by_user(cls, user):
        return cls.objects.get_or_create(user=user)[0]

    @classmethod
    def by_postulant(cls, postulant):
        return cls.by_user(postulant.user)


class PostulantAttachCV(models.Model):
    """Postulan CV's files type word, pdf, etc"""

    user = models.ForeignKey(
        User,
        null=False,
        blank=False,
        related_name='postulant_attachcv')

    name = models.CharField(
        max_length=100,
        null=False,
        blank=False,
        verbose_name=_(u"Nombre")
    )

    attach = models.FileField(
        upload_to=get_attachcv_directory,
        null=False,
        blank=False,
        verbose_name=_(u"CV Anexo"))

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def url(self):
        return resolve_media_url(self.attach.path)

    class Meta:
        unique_together = (("user", "name"), )
