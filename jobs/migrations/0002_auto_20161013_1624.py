# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-10-13 19:24
from __future__ import unicode_literals

from django.db import migrations, models
import django_extensions.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='area',
            name='slug',
            field=django_extensions.db.fields.AutoSlugField(blank=True, editable=False, max_length=40, populate_from=('name',), unique=True, verbose_name='slug'),
        ),
        migrations.AddField(
            model_name='subarea',
            name='slug',
            field=django_extensions.db.fields.AutoSlugField(blank=True, editable=False, max_length=40, populate_from=('name',), unique=True, verbose_name='slug'),
        ),
        migrations.AlterField(
            model_name='job',
            name='get_cvs_ctrl_panel',
            field=models.BooleanField(default=True, verbose_name="Recibir los CV's en mi panel de control"),
        ),
        migrations.AlterField(
            model_name='job',
            name='send_cvs_by_mail',
            field=models.BooleanField(default=True, verbose_name='Enviarme una copia por correo electr\xf3nico'),
        ),
    ]
