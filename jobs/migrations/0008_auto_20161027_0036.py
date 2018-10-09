# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-10-27 03:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0007_role_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='area',
            name='description',
            field=models.CharField(blank=True, max_length=300, null=True, verbose_name=b'Descripci\xc3\xb3n'),
        ),
        migrations.AlterField(
            model_name='role',
            name='description',
            field=models.CharField(blank=True, max_length=300, null=True, verbose_name=b'Descripci\xc3\xb3n'),
        ),
        migrations.AlterField(
            model_name='sector',
            name='description',
            field=models.CharField(blank=True, max_length=300, null=True, verbose_name=b'Descripci\xc3\xb3n'),
        ),
        migrations.AlterField(
            model_name='subarea',
            name='description',
            field=models.CharField(blank=True, max_length=300, null=True, verbose_name=b'Descripci\xc3\xb3n'),
        ),
    ]
