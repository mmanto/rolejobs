# encoding=utf-8

from __future__ import unicode_literals
import datetime as dt

from django.utils.translation import gettext as _
from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator

from cities_light.models import (City, Region, Country)

from accounts.models import User
from utils.models import SimpleItemModel, SlugedModel
from employer.models import Employer
from education.models import Language
from education.choices import EDUCATION_GRADES

JOB_TYPE_FULLTIME = 1
JOB_TYPE_PARTTIME = 2
JOB_TYPE_FREELANCE = 3

JOB_TYPE_CHOICES = (
    (JOB_TYPE_FULLTIME, _(u'Full-Time')),
    (JOB_TYPE_PARTTIME, _(u'Part-Time')),
    (JOB_TYPE_FREELANCE, _(u'Freelance')),
)

JOB_STATUS_PENDING = 10
JOB_STATUS_HAB = 20
JOB_STATUS_SUSPENDED = 30
JOB_STATUS_BANNED = 40
JOB_STATUS_REJECTED = 50
JOB_STATUS_DRAF = 99

JOB_STATUS_CHOICES = {
    (JOB_STATUS_PENDING, _(u"Pendiente")),
    (JOB_STATUS_REJECTED, _(u"Rechazado")),
    (JOB_STATUS_HAB, _(u"Publicado")),
    (JOB_STATUS_SUSPENDED, _(u"Suspendido")),
    (JOB_STATUS_BANNED, _(u"Baneado")),
    (JOB_STATUS_DRAF, _(u"Borrador"))
}

JOB_MODERATOR_STATUS_CHOICES = {
    (JOB_STATUS_HAB, _(u"Habilitar")),
    (JOB_STATUS_REJECTED, _(u"Rechazar")),
    (JOB_STATUS_BANNED, _(u"Banear")),
}

QUESTION_TYPE_TEXT = 0x00
QUESTION_TYPE_NUMBER = 0x10
QUESTIONS_TYPE_BOOLEAN = 0x20
QUESTION_TYPE_CHOICES = 0x30

QUESTIONS_TYPES = (
    (QUESTION_TYPE_TEXT, _(u"Texto")),
    (QUESTION_TYPE_NUMBER, _(u"Númerica")),
    (QUESTIONS_TYPE_BOOLEAN, _(u"Si/no")),
    (QUESTION_TYPE_CHOICES, _(u"Multiple choices")),
)

POSTULATION_NEW = 0x00
POSTULATION_ACCEPTED = 0x10
POSTULATION_REJECTED = 0x20

POSTULATIONS_CHOICES = (
    (POSTULATION_NEW, _(u"Nueva")),
    (POSTULATION_ACCEPTED, _(u"Aceptada")),
    (POSTULATION_REJECTED, _(u"Rechazada")),
)

GENDER_CHOICES = (
    (1, _('Masculino')),
    (2, _('Femenino')),
    (99, _('Otro')),
)


class InsufficientPostPointsException(Exception):
    pass


class NotReachPublishDate(Exception):
    pass


class Area(SlugedModel):
    """Job area"""
    pass


class SubArea(SlugedModel):
    """Job sub area"""

    area = models.ForeignKey(
        Area,
        null=False,
        blank=False,
        related_name="subareas"
    )


class Hierarchy(SimpleItemModel):
    """Hierarchy model"""
    pass


class TitleRole(SimpleItemModel):
    """Title role"""
    pass


class Position(SimpleItemModel):
    """Job position"""
    pass


class Role(SlugedModel):
    """Job Role"""
    pass


class BranchActivity(SimpleItemModel):
    """Job branch activity"""
    pass


class Technology(SlugedModel):
    """Technology"""

    class Meta:
        verbose_name = _('Technology')
        verbose_name_plural = _('Technologies')


class SubTechnology(SlugedModel):
    """Sub technologies"""

    technology = models.ForeignKey(
        Technology,
        null=False,
        blank=False,
        related_name="subtechnologies")

    class Meta:
        verbose_name = _('Subtechnology')
        verbose_name_plural = _('Subtechnologies')


class Job(models.Model):
    """Job model"""

    owner = models.ForeignKey(
        Employer,
        related_name="jobs",
        related_query_name="job",
        null=False)

    confidential = models.BooleanField(
        null=False,
        default=False,
        verbose_name=_(u"Confidencial")
    )

    status = models.IntegerField(
        null=False,
        default=JOB_STATUS_PENDING,
        choices=JOB_STATUS_CHOICES,
        verbose_name=_(u"Estado"))

    title = models.CharField(
        max_length=100,
        null=False,
        blank=False,
        verbose_name=_("Título del aviso"))

    reference_number = models.BigIntegerField(
        null=True,
        blank=True,
        verbose_name=_("Número de referencia"))

    contract_date = models.DateField(
        null=True,
        blank=True,
        verbose_name=_("Fecha de contratación")
    )

    description = models.TextField(
        null=False,
        blank=False,
        verbose_name=_("Descripción del puesto"))

    role = models.ForeignKey(
        TitleRole,
        null=False,
        blank=False,
        verbose_name=_('Rol'))

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

    roles = models.ManyToManyField(
        Role,
        verbose_name=_(u"Roles"))

    branch_activity = models.ForeignKey(
        BranchActivity,
        null=False,
        blank=False,
        verbose_name=_('Ramo o actividad'))

    handicapped_postulant = models.BooleanField(
        null=False,
        default=True,
        verbose_name=_("Postulantes discapacitados"))

    show_address = models.BooleanField(
        null=False,
        default=True,
        verbose_name=_("Mostrar dirección en el aviso"))

    get_cvs_ctrl_panel = models.BooleanField(
        null=False,
        default=True,
        verbose_name=_(u"Recibir los CV's en mi panel de control"))

    send_cvs_by_mail = models.BooleanField(
        null=False,
        default=True,
        verbose_name=_(u"Enviarme una copia por correo electrónico"))

    send_gratitude_by_mail = models.BooleanField(
        null=False,
        default=False,
        verbose_name=_(u"Enviar email de agradecimiento al postularse"))

    area = models.ForeignKey(
        Area,
        null=False,
        blank=False,
        verbose_name=_("Area de publicación"))

    subarea = models.ForeignKey(
        SubArea,
        null=False,
        blank=False,
        verbose_name=_("Sector"))

    job_type = models.IntegerField(
        null=False,
        blank=False,
        choices=JOB_TYPE_CHOICES,
        verbose_name=_("Tipo de trabajo"))

    duration_of_publishing = models.DurationField(
        default=dt.timedelta(days=30))

    featured = models.BooleanField(
        null=False,
        default=False,
        verbose_name=_(u"Destacado"))

    published = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_(u"Publicado"))

    created = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_(u"Creado"))

    updated = models.DateTimeField(
        auto_now=True,
        verbose_name=_(u"Modificado"))

    moderated = models.BooleanField(
        null=False,
        blank=False,
        default=False,
        verbose_name=_(u"Fue moderado"))

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
        null=False,
        blank=False,
        verbose_name=_("Provincia"))

    country = models.ForeignKey(
        Country,
        null=False,
        blank=False,
        verbose_name=_(u"País"))

    residence_range = models.FloatField(
        null=True,
        blank=True,
        verbose_name=_(u"Rango de residencia")
    )

    residence_range_exclusive = models.BooleanField(
        null=False,
        blank=False,
        default=False,
        verbose_name=_(u"Es excluyente"))

    vacancies = models.IntegerField(
        null=True,
        blank=True,
        verbose_name=_(u"Cantidad de vacantes")
    )

    publish_date = models.DateField(
        null=True,
        blank=True,
        verbose_name=_(u"Fecha de publicación")
    )

    video = models.URLField(
        null=True,
        blank=True,
        verbose_name=(u"Video")
    )

    # Requirement "statics"
    requirement_driver_license = models.BooleanField(
        null=False,
        blank=False,
        default=False,
        verbose_name=_(u"Licencia de conducir")
    )

    requirement_gender = models.IntegerField(
        null=True,
        choices=GENDER_CHOICES,
        verbose_name=_(u"Género"))

    requirement_age_min = models.IntegerField(
        null=True,
        verbose_name=_(u"Edad minima"),
        validators=[MinValueValidator(1), MaxValueValidator(99)]
    )

    requirement_age_max = models.IntegerField(
        null=True,
        verbose_name=_(u"Edad maxima"),
        validators=[MinValueValidator(1), MaxValueValidator(99)]
    )

    @property
    def requirement_gender_text(self):
        label = [l for v, l in GENDER_CHOICES if v == self.gender]
        if len(label):
            return label[0]
        else:
            return None

    @property
    def geodata_original(self):

        return {
            "country": self.country,
            "region": self.region,
            "city": self.city,
            "address": self.address}

    @property
    def geodata(self):
        geodata = self.geodata_original

        if not self.show_address:
            geodata.update({"address": None})

        return geodata

    @property
    def status_text(self):
        co = [v for i, v in JOB_STATUS_CHOICES if i == self.status]
        return co[0]

    @property
    def job_type_text(self):
        co = [v for i, v in JOB_TYPE_CHOICES if i == self.job_type]
        return co[0]

    @property
    def moderation_object(self):
        return JobForModeration.objects.get(id=self.pk)

    @property
    def is_hab(self):
        return self.status == JOB_STATUS_HAB

    @property
    def postulants_number(self):
        return self.postulants.all().count()

    def get_url(self):
        return u"not_implemented"

    def publish(self):

        if self.status == JOB_STATUS_BANNED:
            raise Exception("Not way")

        if self.owner.post_points >= 10:
            if self.publish_date and dt.date.today() < self.publish_date:
                raise NotReachPublishDate("The publish date is in the future")

            ins = self.moderation_object.moderate(None, JOB_STATUS_HAB,
                                                  u"Puntaje suficiente")
            self.published = ins.published
            self.status = ins.status

            self.save()

            self.owner.use_post_points(10)
        else:
            raise InsufficientPostPointsException("Not sufficient points")

    def get_user_postulation(self, user):
        return self.postulants.get(user=user)

    def __unicode__(self):
        return u"%s" % self.title

    class Meta:
        permissions = (
            ('can_moderate', 'Can moderate jobs'),
        )


class JobsForModerationManager(models.Manager):
    """Manager for JobForModeration"""

    def create(self, *args, **kwargs):
        raise Exception("Use jobs.Job")


class JobForModeration(Job):

    def save(*args, **kwargs):
        raise Exception("Not implemented. use jobs.Job")

    def moderate(self, user, status, reason=""):
        last_status = self.status

        if not status == JOB_STATUS_HAB and last_status == status:
            return

        self.status = status
        sh = None

        try:
            sh = self.moderation_history.create(
                old_status=last_status,
                new_status=status,
                action_by=user,
                reason=reason)

            if user is not None:

                self.moderated = True

                if status == JOB_STATUS_BANNED:
                    # if a job is banned, disscount 50 post points
                    self.owner.use_post_points(50)
                elif status == JOB_STATUS_REJECTED:
                    # if a job is on pending, disscount 30 post points
                    self.owner.use_post_points(30)
                elif last_status == JOB_STATUS_REJECTED and (
                     status == JOB_STATUS_HAB):
                    # if a job is enabled after rejected, give 10 post points
                    self.owner.use_post_points(10)
                elif last_status == JOB_STATUS_PENDING and (
                     status == JOB_STATUS_HAB):
                    # if a job is enabled after pendding, give 30 post points
                    self.owner.use_post_points(-30)

            else:
                self.moderated = False

            if status == JOB_STATUS_HAB:
                self.published = dt.datetime.now()

            super(JobForModeration, self).save()
            sh.save()
        except Exception as e:
            self.status = last_status
            super(JobForModeration, self).save()
            if sh:
                sh.delete()
            raise e

        return self

    class Meta:
        proxy = True
        ordering = ("updated", "created")
        verbose_name = _(u"Job for moderation")
        verbose_name_plural = _(u"Jobs for moderation")


class JobModerationHistory(models.Model):
    """Job moderation history"""

    job = models.ForeignKey(
        Job,
        null=False,
        blank=False,
        related_name="moderation_history")

    old_status = models.IntegerField(
        null=False,
        default=JOB_STATUS_DRAF,
        choices=JOB_STATUS_CHOICES,
        verbose_name=_(u"Cambiado de"))

    new_status = models.IntegerField(
        null=False,
        default=JOB_STATUS_DRAF,
        choices=JOB_STATUS_CHOICES,
        verbose_name=_(u"Cambiado a"))

    action_by = models.ForeignKey(
        User,
        null=True,
        blank=True,
        verbose_name=_("Moderado por"))

    action_date = models.DateTimeField(
        null=False,
        blank=False,
        auto_now_add=True)

    reason = models.CharField(
        max_length=512,
        null=True,
        blank=True,
        verbose_name=_(u"Razón"))

    @property
    def old_status_text(self):
        co = [v for i, v in JOB_STATUS_CHOICES if i == self.old_status]
        if not len(co):
            return "?"
        return co[0]

    @property
    def new_status_text(self):
        co = [v for i, v in JOB_STATUS_CHOICES if i == self.new_status]
        if not len(co):
            return "?"
        return co[0]

    @property
    def by(self):
        if self.action_by:
            return u"%s" % self.action_by
        else:
            return u"<auto>"

    def __unicode__(self):

        if self.old_status == self.new_status:
            return u"Status confirmed to %s by %s" % (
                self.new_status_text,
                self.by
            )
        else:
            return u"Status changed from %s to %s by %s" % (
                self.old_status_text,
                self.new_status_text,
                self.by
            )

    class Meta:
        ordering = ('-action_date', )


class Requirement(models.Model):
    """Job Requirement"""

    job = models.ForeignKey(
        Job,
        null=False,
        blank=False,
        related_name="requirements")

    exclusive = models.BooleanField(
        null=False,
        blank=False,
        default=True,
        verbose_name=_(u"Es excluyente"))

    description = models.CharField(
        max_length=250,
        null=False,
        blank=False,
        verbose_name=_(u"Requisito"))

    def __unicode__(self):
        u = u"%s" % self.description

        if self.exclusive:
            u += u" (%s)" % _(u"Excluyente")

        return u


class LanguageRequirement(models.Model):
    """Job language requirement"""

    job = models.ForeignKey(
        Job,
        null=False,
        blank=False,
        related_name="language_requirements")

    exclusive = models.BooleanField(
        null=False,
        blank=False,
        default=True,
        verbose_name=_(u"Es excluyente"))

    language = models.ForeignKey(
        Language,
        null=False,
        blank=False,
        verbose_name=_(u"Lenguaje"))

    level = models.IntegerField(
        null=False,
        blank=False,
        verbose_name=_(u"Nivél mínimo"))

    @property
    def name(self):
        return u"%s" % self.language.name

    def clean(self):

        if self.level < 0 or self.level > 10:
            raise ValidationError(_(u"El nivél debe ser un número entre " +
                                    u"1 y 10"))

    def __unicode__(self):
        u = u"%s" % self.language.name

        if self.exclusive:
            u += u" (%s)" % _(u"Excluyente")

        return u


class EducationRequirement(models.Model):
    """Job education Requirement"""

    job = models.OneToOneField(
        Job,
        null=False,
        blank=False,
        related_name="education_requirement")

    exclusive = models.BooleanField(
        null=False,
        blank=False,
        default=True,
        verbose_name=_(u"Es excluyente"))

    level = models.IntegerField(
        null=False,
        blank=False,
        choices=EDUCATION_GRADES,
        verbose_name=_(u"Nivél de educación mínimo"))

    finished = models.BooleanField(
        null=False,
        blank=False,
        default=False,
        verbose_name=_(u"Terminado"))

    @property
    def level_text(self):
        label = [l for v, l in EDUCATION_GRADES if v == self.level]
        if len(label):
            return label[0]
        else:
            return None

    def __unicode__(self):
        return "%s %s %s" % (
            self.level_text,
            _(u"Terminado") if self.finished else "Cursando",
            _(u"(Exluyente)") if self.exclusive else "",
        )


class KnowledgeRequirement(models.Model):
    """knowledge requirement for job"""

    job = models.ForeignKey(
        Job,
        null=False,
        blank=False,
        related_name="knowledge_requirements")

    exclusive = models.BooleanField(
        null=False,
        blank=False,
        default=True,
        verbose_name=_(u"Es excluyente"))

    technology = models.ForeignKey(
        Technology,
        null=False,
        blank=False,
        verbose_name=_(u"Sector tecnologico"))

    subtechnology = models.ForeignKey(
        SubTechnology,
        null=False,
        blank=False,
        verbose_name=_(u"Tecnología"))

    hierarchy = models.ForeignKey(
        Hierarchy,
        null=False,
        blank=False,
        verbose_name=_(u"Nivél"))

    def __unicode__(self):
        u = "%s > %s (%s)" % (
            self.technology.name,
            self.subtechnology.name,
            self.hierarchy.name
        )

        if self.exclusive:
            u += _(u" excluyente")

        return u


class Question(models.Model):
    """Job question"""

    job = models.ForeignKey(
        Job,
        null=False,
        blank=False,
        related_name="questions")

    is_required = models.BooleanField(
        null=False,
        blank=False,
        default=False,
        verbose_name=_(u"¿Es requerida?"))

    question_type = models.PositiveSmallIntegerField(
        null=False,
        blank=False,
        choices=QUESTIONS_TYPES,
        verbose_name=_(u"Tipo de pregunta"))

    question = models.CharField(
        max_length=300,
        null=False,
        blank=False,
        verbose_name=_(u"Pregunta"))

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def type_text(self):
        co = [v for i, v in QUESTIONS_TYPES if i == self.question_type]
        return co[0]

    def validate_reponse(self, response):
        if self.question_type == QUESTION_TYPE_TEXT:
            return True
        elif self.question_type == QUESTION_TYPE_NUMBER:
            return True
        elif self.question_type == QUESTIONS_TYPE_BOOLEAN:
            return True
        elif self.question_type == QUESTION_TYPE_CHOICES:
            return True
        else:
            raise Exception("Inválid type")

    def __unicode__(self):
        return u"%s" % self.question


class QuestionOption(models.Model):
    """Options for multiple choices questions"""

    question = models.ForeignKey(
        Question,
        null=False,
        blank=False,
        related_name="options")

    text = models.CharField(
        max_length=300,
        null=False,
        blank=False,
        verbose_name=_(u"Respuesta"))

    is_correct = models.BooleanField(
        null=False,
        blank=False,
        default=False,
        verbose_name=_(u"Correcta"))

    def __unicode__(self):
        return u"%s" % self.text


class JobPostulation(models.Model):

    user = models.ForeignKey(
        User,
        null=False,
        blank=False,
        related_name="postulations",
        verbose_name=_(u"Postulante"))

    job = models.ForeignKey(
        Job,
        null=False,
        blank=False,
        related_name="postulants",
        verbose_name=_(u"Oferta de trabajo"))

    status = models.PositiveSmallIntegerField(
        null=False,
        blank=False,
        default=POSTULATION_NEW,
        choices=POSTULATIONS_CHOICES,
        verbose_name=_(u"Estado"))

    request_salary = models.PositiveIntegerField(
        null=True,
        default=None,
        verbose_name=_(u"Salario pretendido"))

    message = models.CharField(
        max_length=2080,
        null=False,
        blank=False,
        verbose_name=_(u"¿Por qué pienza que es el indicado?"))

    date = models.DateTimeField(
        null=False,
        auto_now_add=True,
        verbose_name=_(u"Fecha de postulación"))

    questions_answers = models.ManyToManyField(
        Question,
        through='QuestionAnswer',
        through_fields=('postulation', 'question'),
        verbose_name=_(u"Respuestas"),
        related_name="answers")

    read = models.BooleanField(
        null=False,
        default=False,
        verbose_name=_(u"Leída"))

    favorite = models.BooleanField(
        null=False,
        default=False,
        verbose_name=_(u"Favorito")
    )

    @property
    def status_text(self):
        co = [v for i, v in POSTULATIONS_CHOICES if i == self.status]
        return co[0]

    def mark_read(self):
        if not self.read:
            self.read = True
            self.save()

    def set_status(self, status):
        if status not in [i for i, v in POSTULATIONS_CHOICES]:
            raise Exception("Unknow status")

        if status == POSTULATION_NEW:
            raise Exception("Status can't return to new")

        if not status == self.status:
            self.status = status
            self.save()

    class Meta:
        unique_together = (("job", "user"),)


class QuestionAnswer(models.Model):
    """Question response"""

    postulation = models.ForeignKey(
        JobPostulation,
        related_name="questionsanswers",
        on_delete=models.CASCADE)

    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE)

    data_response = models.CharField(
        max_length=500,
        null=True,
        blank=True,
        default=None)

    data_option = models.ForeignKey(
        QuestionOption,
        null=True,
        blank=True,
        default=None)

    def set_response(self, response):
        question_type = self.question.question_type

        if question_type == QUESTION_TYPE_TEXT:
            self.data_response = u"%s" % response
        elif question_type == QUESTION_TYPE_NUMBER:
            self.data_response = u"%i" % response
        elif question_type == QUESTIONS_TYPE_BOOLEAN:
            self.data_response = u"%s" % str(bool(response))
        elif question_type == QUESTION_TYPE_CHOICES:
            option = self.question.options.get(id=int(response))
            self.data_option = option
        else:
            raise Exception("Unknow question type %i" % question_type)

    @property
    def response(self):
        question_type = self.question.question_type

        if question_type == QUESTION_TYPE_TEXT:
            return u"%s" % self.data_response
        elif question_type == QUESTION_TYPE_NUMBER:
            return int(self.data_response)
        elif question_type == QUESTIONS_TYPE_BOOLEAN:
            return self.data_response == "True"
        elif question_type == QUESTION_TYPE_CHOICES:
            return self.data_option
        else:
            raise Exception("Unknow question type %i" % question_type)

    def __unicode__(self):
        return "%s answer" % self.question.question


class JobPostulationNote(models.Model):
    """Notes for job postulations"""

    postulation = models.ForeignKey(
        JobPostulation,
        related_name="jobpostulation_notes",
        on_delete=models.CASCADE)

    title = models.CharField(
        max_length=100,
        null=False,
        blank=False,
        verbose_name=_("Título"))

    body = models.TextField(
        null=False,
        blank=False,
        verbose_name=_("Nota"))
