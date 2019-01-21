# encoding=utf-8

from django.utils.translation import gettext as _

MARRIED_STATUS = (
    (1, _("Soltera/o")),
    (2, _("Casada/o")),
    (3, _("Divorsiada/o")),
    (4, _("Viuda/o"))
)

LICENSE_TYPE_1 = 1
LICENSE_TYPE_2 = 2
LICENSE_TYPE_3 = 3

TYPE_LICENCE = (
    (99, _('Ningúna')),
    (LICENSE_TYPE_1, _('Auto')),
    (LICENSE_TYPE_2, _('Motocicleta')),
    (LICENSE_TYPE_3, _('Profesional')),
)

YES_NO_CHOICES = (
    (True, _("Si")),
    (False, _("No"))
)

WORK_TYPE = (
    ("Efectivo", _("Efectivo")),
    ("Freelance", _("Freelance")),
    ("Indiferente", _("Indiferente")),
    ("Pasantia", _("Pasantia")),
    ("PlazoFijo", _("Plazo Fijo")),
    ("PorTemporadas", _("Por Temporadas")),
    ("Temporal", _("Temporal"))
)

STAFF_CHARGE = (
    ("1", "Sin personal a cargo"),
    ("2", "1 a 5"),
    ("3", "6 a 10"),
    ("4", "11 a 20"),
    ("5", "21 a 50"),
    ("6", "51 a 100"),
    ("7", "Más de 100")
)

REFERENCE_TYPE_COWORKER = 1
REFERENCE_TYPE_LEADER = 2
REFERENCE_TYPE_EMPLOYER = 3
REFERENCE_TYPE_EMPLOYEE = 4
REFERENCE_TYPE_OTHER = 99

REFERENCE_TYPES = (
    (REFERENCE_TYPE_COWORKER, _(u"Compañero de trabajo")),
    (REFERENCE_TYPE_LEADER, _(u"Estaba a su cargo")),
    (REFERENCE_TYPE_EMPLOYER, _(u"Era mi jefe")),
    (REFERENCE_TYPE_EMPLOYEE, _(u"Estaba a mi cargo")),
    (REFERENCE_TYPE_OTHER, _("Otro")),
)

USD_TYPE = 'USD'
AR_PESO_TYPE = 'ARS'

CURRENCY_CHOICES = (
    (USD_TYPE, _('Dólar estadounidense')),
    (AR_PESO_TYPE, _('Peso argentino')),
)

COMPLETION_PROFILE = 1
COMPLETION_BIO = 2
COMPLETION_EXPERIENCES = 4
COMPLETION_EDUCATION = 8
COMPLETION_LANGUAGES = 16
COMPLETION_REFERENCES = 32
COMPLETION_AVATAR = 64
COMPLETION_COMPUTERKNOWLEDGE = 128
COMPLETION_ADDITIONALKNOWLEDGES = 256

CV_COMPLETION = (
    (COMPLETION_PROFILE, _(u"Datos de perfíl")),
    (COMPLETION_BIO, _(u"Biografía")),
    (COMPLETION_EXPERIENCES, _(u"Experiencias laborales")),
    (COMPLETION_EDUCATION, _(u"Educación")),
    (COMPLETION_LANGUAGES, _(u"Idiomas")),
    (COMPLETION_REFERENCES, _(u"Referencias")),
    (COMPLETION_AVATAR, _(u"Foto de perfíl")),
    (COMPLETION_COMPUTERKNOWLEDGE, _(u"Conocimientos informáticos")),
    (COMPLETION_ADDITIONALKNOWLEDGES, _(u"Conocimientos adicionales"))
)
