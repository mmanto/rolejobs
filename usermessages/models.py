from __future__ import unicode_literals

from django.db import models
from django.utils.translation import ugettext_lazy as _

from accounts.models import User
from jobs.models import JobPostulation
from employer.models import CVRequest


class UserMessage(models.Model):
    """Internal Users Message"""

    employer = models.ForeignKey(
        User,
        null=False,
        blank=False,
        related_name='message_employer'
    )

    postulant = models.ForeignKey(
        User,
        null=False,
        blank=False,
        related_name='message_postulant'
    )

    postulation = models.ForeignKey(
        JobPostulation,
        null=True,
        blank=True,
        related_name='message_postulation'
    )

    cvrequest = models.ForeignKey(
        CVRequest,
        null=True,
        blank=True,
        related_name='message_cv_request'
    )

    response = models.ForeignKey(
        'UserMessage',
        null=True,
        blank=True,
        related_name='message_response'
    )

    message = models.TextField(
        null=False,
        blank=False,
        verbose_name=_("Mensaje")
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    readed_at = models.DateTimeField(null=True, blank=True)
