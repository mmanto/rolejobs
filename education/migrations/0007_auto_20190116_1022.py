# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2019-01-16 15:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('education', '0006_usereducation_career'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usereducation',
            name='career',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Carrera'),
        ),
    ]
