# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2019-01-11 19:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('postulant', '0008_auto_20170215_0139'),
    ]

    operations = [
        migrations.AddField(
            model_name='professionalexperience',
            name='company_address',
            field=models.CharField(default='', max_length=100, verbose_name=b'Direcci\xc3\xb3n'),
            preserve_default=False,
        ),
    ]
