# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-11-16 20:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0021_auto_20161116_1701'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job',
            name='created',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Creado'),
        ),
        migrations.AlterField(
            model_name='job',
            name='featured',
            field=models.BooleanField(default=False, verbose_name='Destacado'),
        ),
        migrations.AlterField(
            model_name='job',
            name='published',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Publicado'),
        ),
        migrations.AlterField(
            model_name='job',
            name='status',
            field=models.IntegerField(choices=[(20, 'Publicado'), (10, 'Pendiente'), (99, 'Borrador'), (50, 'Rechazado'), (40, 'Baneado'), (30, 'Suspendido')], default=10, verbose_name='Estado'),
        ),
        migrations.AlterField(
            model_name='job',
            name='updated',
            field=models.DateTimeField(auto_now=True, verbose_name='Modificado'),
        ),
    ]
