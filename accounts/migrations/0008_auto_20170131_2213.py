# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2017-02-01 01:13
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cities_light', '0006_compensate_for_0003_bytestring_bug'),
        ('accounts', '0007_auto_20161111_0626'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='city',
        ),
        migrations.AddField(
            model_name='profile',
            name='address',
            field=models.CharField(default=None, max_length=100, verbose_name='Direccion'),
        ),
        migrations.AddField(
            model_name='profile',
            name='city',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='cities_light.City', verbose_name='Ciudad'),
        ),
        migrations.AddField(
            model_name='profile',
            name='country',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='cities_light.Country', verbose_name='Pa\xeds'),
        ),
        migrations.AddField(
            model_name='profile',
            name='region',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='cities_light.Region', verbose_name='Provincia'),
        ),
    ]
