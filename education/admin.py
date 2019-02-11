from django.contrib import admin

# Register your models here.

from models import EducationArea, Computerknowledge, Additionalknowledge, Workpreference
  

admin.site.register(EducationArea)
admin.site.register(Computerknowledge)
admin.site.register(Additionalknowledge)
admin.site.register(Workpreference)
