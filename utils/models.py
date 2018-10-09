# encoding=utf-8

from django.db import models
from django.utils.translation import gettext as _

from django_extensions.db.fields import AutoSlugField


class SimpleItemModel(models.Model):
    """Simple abstract model"""

    name = models.CharField(
        max_length=100,
        null=False,
        blank=False,
        verbose_name=_("Nombre"))

    def __unicode__(self):
        return "%s" % self.name

    class Meta:
        abstract = True


class SimpleItemDescModel(SimpleItemModel):
    """Like SimpleItemModel, but with description"""

    description = models.CharField(
        max_length=300,
        null=True,
        blank=True,
        verbose_name=_("Descripción"))

    class Meta:
        abstract = True


class SlugedModel(SimpleItemDescModel):
    """Like SimpleItemDescModel but with a slug field"""

    slug = AutoSlugField(
        _('slug'),
        max_length=40,
        unique=True,
        populate_from=('name',))

    class Meta:
        abstract = True
