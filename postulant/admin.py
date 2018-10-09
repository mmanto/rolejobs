# encoding=utf-8

from django.contrib import admin

from postulant import models

admin.site.register([
    models.Postulant,
    models.Biographic,
    models.ProfessionalExperience,
])
