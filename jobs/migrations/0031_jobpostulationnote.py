# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2017-04-12 02:26
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0030_auto_20170406_1046'),
    ]

    operations = [
        migrations.CreateModel(
            name='JobPostulationNote',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='T\xedtulo')),
                ('body', models.TextField(verbose_name='Nota')),
                ('postulation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='jobpostulation_notes', to='jobs.JobPostulation')),
            ],
        ),
    ]
