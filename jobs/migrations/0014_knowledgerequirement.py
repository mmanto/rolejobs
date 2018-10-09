# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-10-28 22:05
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0013_auto_20161028_1853'),
    ]

    operations = [
        migrations.CreateModel(
            name='knowledgeRequirement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('exclusive', models.BooleanField(default=True, verbose_name='Es excluyente')),
                ('hierarchy', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='jobs.Hierarchy', verbose_name='Niv\xe9l')),
                ('job', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='knowledge_requirements', to='jobs.Job')),
                ('subtechnology', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='jobs.SubTechnology', verbose_name='Tecnolog\xeda')),
                ('technology', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='jobs.Technology', verbose_name='Sector tecnologico')),
            ],
        ),
    ]
