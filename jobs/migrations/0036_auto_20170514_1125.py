# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2017-05-14 14:25
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0035_job_residence_range_exclusive'),
    ]

    operations = [
        migrations.AddField(
            model_name='job',
            name='requirement_age_max',
            field=models.IntegerField(null=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(99)], verbose_name='Edad maxima'),
        ),
        migrations.AddField(
            model_name='job',
            name='requirement_age_min',
            field=models.IntegerField(null=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(99)], verbose_name='Edad minima'),
        ),
        migrations.AddField(
            model_name='job',
            name='requirement_driver_license',
            field=models.NullBooleanField(verbose_name='Licencia de conducir'),
        ),
        migrations.AddField(
            model_name='job',
            name='requirement_gender',
            field=models.IntegerField(choices=[(1, 'Masculino'), (2, 'Femenino'), (99, 'Otro')], null=True, verbose_name='G\xe9nero'),
        ),
    ]
