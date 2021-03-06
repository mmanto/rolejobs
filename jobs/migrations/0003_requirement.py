# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-10-14 05:16
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0002_auto_20161013_1624'),
    ]

    operations = [
        migrations.CreateModel(
            name='Requirement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('exclusive', models.BooleanField(default=True, verbose_name='Es excluyente')),
                ('description', models.CharField(max_length=250, verbose_name='Requisito')),
                ('job', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Requisitos', to='jobs.Job')),
            ],
        ),
    ]
