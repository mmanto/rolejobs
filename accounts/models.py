# -*- coding: utf8 -*-

from __future__ import unicode_literals

import hashlib
import random
from datetime import datetime

from django.core import urlresolvers
from django.db import models
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.models import (
    BaseUserManager,
    AbstractBaseUser,
    PermissionsMixin,
    Permission,
)

from django.contrib.auth.tokens import default_token_generator

from django.utils.translation import ugettext as _
# from django.dispatch import receiver
# from django.db.models.signals import post_save

# Secret key for hash-valitador generators
from django.conf import settings

from polymorphic.models import PolymorphicModel
from emailspool.models import Spool
from cities_light.models import (City, Region, Country)

TYPE_ROLE = (
    ('postulant', 'postulant'),
    ('employer', 'employer')
)

GENDER_CHOICES = (
    (None, _('Género')),
    (1, _('Masculino')),
    (2, _('Femenino')),
    (99, _('Otro')),
)


def create_validation_hash(email):
    """Generate a validation hash, for check the email"""
    v_hash = hashlib.sha1(email + settings.SECRET_KEY + str(random.random()))
    return v_hash.hexdigest()


class AccountUserManager(BaseUserManager):

    def create_user(self, email, password, *args, **kargs):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            **kargs
        )

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(email, password=password)

        user.is_admin = True
        user.status = user.S_ENABLED
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

    @property
    def moderators(self):
        perm = Permission.objects.get(codename="can_moderate")
        return self.filter(
           models.Q(groups__permissions=perm) | models.Q(user_permissions=perm)
        ).distinct()


class User(AbstractBaseUser, PermissionsMixin):
    """User model"""

    S_NEW = 0
    S_ENABLED = 10
    S_BANNED = 20

    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )

    # Only for a bug in rest_auth
    username = models.CharField(
        max_length=1,
        null=True,
        blank=True)

    first_name = models.CharField(max_length=250, blank=True, null=True,
                                  default=None)
    last_name = models.CharField(max_length=250,
                                 blank=True, null=True, default=None)
    status = models.SmallIntegerField(default=S_NEW, null=False, blank=False)
    is_staff = models.BooleanField(
        default=False,
        help_text=_('Designates whether the user can log into this admin '
                    'site.'))
    is_active = models.BooleanField(default=True)

    is_admin = models.BooleanField(default=False)

    type_profile = models.CharField(max_length=10, choices=TYPE_ROLE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    email_validation_hash = models.CharField(max_length=40, null=True,
                                             default=None, blank=True)

    last_profile_update = models.DateTimeField(
        auto_now_add=True)

    completed_items = models.PositiveSmallIntegerField(
        null=False,
        default=0)

    objects = AccountUserManager()

    USERNAME_FIELD = 'email'
    # REQUIRED_FIELDS = ['username']

    @property
    def profile(self):
        return Profile.objects.get(user=self)[0]

    @property
    def is_postulant(self):
        return self.type_profile == 'postulant'

    @property
    def is_employer(self):
        return self.type_profile == 'employer'

    def set_complete(self, item):
        self.completed_items = self.completed_items | item
        self.last_profile_update = datetime.now()
        self.save()

    def send_validation_email(self):
        """Send the email with validation hash"""

        self.email_validation_hash = create_validation_hash(
            self.email)

        self.save()

        email = Spool.create_by_layout('accountvalidation', {
            'name': str(self),
            'hash': self.email_validation_hash,
            'id': self.id})

        email.to = self.email
        email.subject = _(u"Valida tu cuenta de RoleJobs")
        email.save()

    def send_reset_password_email(self):
        token = default_token_generator.make_token(self)

        email = Spool.create_by_layout('resetpassword', {
            'name': str(self),
            'token': token,
            'id': urlsafe_base64_encode(str(self.id))})

        email.to = self.email
        email.subject = _(u"Cambio de contraseña en RoleJobs")
        email.save()

    def send_moderation_email(self, job):
        """Send the email with a moderation is needed"""

        if not self.has_perm("jobs.can_moderate"):
            raise Exception("Not perms")

        url = urlresolvers.reverse("admin:moderate_job", args=(job.id,))

        email = Spool.create_by_layout('moderationneeded', {
            'name': str(self),
            "url": url,
            'job': job
        })

        email.to = self.email
        email.subject = _(u'Se necesita moderación')
        email.save()

    def send_usermessage_email(self, message):
        """Send the email if new user message"""

        url = urlresolvers.reverse("usermessage-retrieve", args=(message.id,))

        email = Spool.create_by_layout('newmessage', {"url": url})

        email.to = self.email
        email.subject = _(u'Nuevo mensaje')
        email.save()

    def send_courses_postulation_notification(self, course):
        """Send notifications to owner of course"""
        if not self.is_postulant:
            raise Exception("Only postulant can send email")

        if not course.notify_by_email:
            raise Exception("Owner of course not want notify by email")

        url = urlresolvers.reverse(
            'courses:courses_by_postulant', args=(course.id))

        email = Spool.create_by_layout('courses_postulation', {
            'name': str(self),
            'url': url,
            'course': course
        })

        email.to = course.owner.email
        email.subject = _(u"Nuevo postulante curso {}".format(course.name))
        email.save()

    def send_postulation_gratitude_notification(self, job_postulation):
        """Send notifications of gratitude for postulation to job"""
        if not self.is_postulant:
            raise Exception("Only postulant can send email")

        job = job_postulation.job

        if not job.send_postulation_gratitude_notification:
            raise Exception(
                "The job not has true the option gratitude by email")

        url = urlresolvers.reverse(
            'postulant:postulant_postulation', args=(job_postulation.id))

        email = Spool.create_by_layout('job_postulation_gratitude', {
            'name': str(self),
            'url': url,
            'job_postulation': job_postulation
        })

        email.to = job_postulation.user.email
        email.subject = _(u"Gracias por postularte {}".format(job.title))
        email.save()

    def calculate_complete(self, items):
        ready = len([i for i in items if self.completed_items & i[0]])
        return round(ready * 100 / len(items))

    def has_completed(self, val):
        return bool(self.completed_items & val)

    def check_validation_code(self, code):
        """Check validation code"""
        return self.email_validation_hash == code

    def get_full_name(self):
        return self.email

    def get_full_role(self):
        return self.type_role

    def get_short_name(self):
        return self.email

    def __unicode__(self):
        return u"%s %s" % (self.first_name, self.last_name)

    def has_perm_role(self, perm):
        if perm in ('postulant', 'postulant'):
            if self.type_role == perm:
                return self.type_role
        return False

    def mark_profile_updated(self):
        self.last_profile_update = datetime.now()
        self.save()


class Profile(PolymorphicModel):

    __perms__ = ('ADMIN', 'EDIT', 'READ', 'GUEST')
    _perms = None

    user = models.OneToOneField(
        User,
        unique=True,
        null=False,
        blank=False)

    gender = models.IntegerField(
        choices=GENDER_CHOICES,
        null=False,
        verbose_name=_('Género'))

    phone_number = models.CharField(
        max_length=100,
        blank=True,
        verbose_name=_('Telefono'))

    mobile_number = models.CharField(
        max_length=100,
        blank=True,
        verbose_name=_('Telefono Celular'))

    address = models.CharField(
        max_length=100,
        null=False,
        blank=False,
        verbose_name=_("Direccion"),
        default=None)

    city = models.ForeignKey(
        City,
        null=True,
        blank=False,
        verbose_name=_("Ciudad"),
        default=None)

    region = models.ForeignKey(
        Region,
        null=False,
        blank=False,
        verbose_name=_("Provincia"),
        default=None)

    country = models.ForeignKey(
        Country,
        null=False,
        blank=False,
        verbose_name=_(u"País"),
        default=None)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def first_name(self):
        return self.user.first_name

    @property
    def last_name(self):
        return self.user.last_name

    @property
    def gender_text(self):
        label = [l for v, l in GENDER_CHOICES if v == self.gender]
        if len(label):
            return label[0]
        else:
            return None

    @property
    def email(self):
        return self.user.email

    @property
    def is_postulant(self):
        return False

    @property
    def is_employer(self):
        return False

    @property
    def get_perms(self):
        if self._perms:
            return self._perms
        return False

    @property
    def geodata(self):
        return {
            "country": self.country,
            "region": self.region,
            "city": self.city,
            "address": self.address}

    def mark_update(self):
        self.user.mark_profile_updated()

    def save(self, *args, **kwargs):
        self.mark_update()
        super(Profile, self).save(*args, **kwargs)

    def set_perms(self, perm):
        if perm in self.__perms__:
            self._perms = perm

    def has_perms(self, perm):
        if self._perm == perm:
            return True
        return False
