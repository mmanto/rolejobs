# encoding=utf-8
from django.contrib import admin

from employer import models

admin.site.register([
    models.Employer,
    models.CVTags,
    models.CVRequest,
])
