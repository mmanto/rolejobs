# encoding: utf-8
from django.utils.translation import gettext as _


CURRENCY_TYPE_USD = 1
CURRENCY_TYPE_EUR = 2
CURRENCY_TYPE_ARS = 3

CURRENCY_TYPE_CHOICES = (
    (CURRENCY_TYPE_USD, _(u'Dolar USA')),
    (CURRENCY_TYPE_EUR, _(u'Euro')),
    (CURRENCY_TYPE_ARS, _(u'Peso Argentina')),
)

COURSE_TYPE_DISTANCE = 1
COURSE_TYPE_CLASSROOM = 2

COURSES_TYPE_CHOICES = (
    (COURSE_TYPE_DISTANCE, _(u'Distancia')),
    (COURSE_TYPE_CLASSROOM, _(u'Presencial')),
)
