# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2017-01-04 10:44
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('education', '0004_load_languages_fixtures'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usereducation',
            name='level',
            field=models.IntegerField(choices=[(2, 'Primario'), (4, 'Secundario'), (8, 'Preparatoria'), (16, 'Terciario'), (1, 'Curso / Capacitaci\xf3n')], verbose_name='Niv\xe9l de educaci\xf3n'),
        ),
    ]
