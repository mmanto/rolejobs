from __future__ import unicode_literals

from django.db import models
from django.utils.translation import ugettext_lazy as _

from accounts.models import User
from postulant.choices import COMPLETION_AVATAR
from rolejobs_api.media import resolve_media_path, resolve_media_url


def get_avatar_directory(instance, filename):
    first_letter = instance.user.email[0]
    path = 'avatars/{0}/{1}-{2}'.format(
        first_letter, instance.user.id, filename)
    return resolve_media_path(path)


class UserAvatar(models.Model):
    """User avatar"""

    user = models.ForeignKey(
        User,
        null=False,
        blank=False,
        related_name='avatars')

    avatar_file = models.ImageField(
        upload_to=get_avatar_directory,
        null=False,
        blank=False,
        verbose_name=_(u"Avatar"))

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_(u"Creado"))

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_(u"Actualizado"))

    label = models.CharField(
        max_length=100,
        null=False,
        blank=False,
        default="default",
        verbose_name="Label")

    @property
    def url(self):
        return resolve_media_url(self.avatar_file.path)

    def save(self, *args, **kwargs):
        self.user.set_complete(COMPLETION_AVATAR)
        super(UserAvatar, self).save(*args, **kwargs)

    def __unicode__(self):
        return "%s avatar" % self.user.email

    class Meta:
        unique_together = (("user", "label"), )
