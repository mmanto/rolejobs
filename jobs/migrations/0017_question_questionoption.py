# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-11-09 03:19
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0016_job_roles'),
    ]

    operations = [
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_required', models.BooleanField(default=False, verbose_name='\xbfEs requerida?')),
                ('question_type', models.PositiveSmallIntegerField(choices=[(0, 'Texto'), (16, 'N\xfamerica'), (32, 'Si/no'), (48, 'Multiple choices')], verbose_name='Tipo de pregunta')),
                ('question', models.CharField(max_length=300, verbose_name='Pregunta')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('job', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='questions', to='jobs.Job')),
            ],
        ),
        migrations.CreateModel(
            name='QuestionOption',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=300, verbose_name='Respuesta')),
                ('is_correct', models.BooleanField(default=False, verbose_name='Correcta')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='options', to='jobs.Question')),
            ],
        ),
    ]
