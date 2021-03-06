# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-12-04 07:56
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('jobs', '0023_job_moderated'),
    ]

    operations = [
        migrations.CreateModel(
            name='JobPostulation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.PositiveSmallIntegerField(choices=[(0, 'Nueva'), (16, 'Aceptada'), (32, 'Rechazada')], default=0, verbose_name='Estado')),
                ('request_salary', models.PositiveIntegerField(default=None, null=True, verbose_name='Salario pretendido')),
                ('message', models.CharField(max_length=2080, verbose_name='\xbfPor qu\xe9 pienza que es el indicado?')),
                ('date', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de postulaci\xf3n')),
                ('job', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='postulants', to='jobs.Job', verbose_name='Oferta de trabajo')),
            ],
        ),
        migrations.CreateModel(
            name='QuestionAnswer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data_response', models.CharField(blank=True, default=None, max_length=500, null=True)),
                ('data_option', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='jobs.QuestionOption')),
                ('postulation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='jobs.JobPostulation')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='jobs.Question')),
            ],
        ),
        migrations.AddField(
            model_name='jobpostulation',
            name='questions_answers',
            field=models.ManyToManyField(related_name='answers', through='jobs.QuestionAnswer', to='jobs.Question', verbose_name='Respuestas'),
        ),
        migrations.AddField(
            model_name='jobpostulation',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='postulations', to=settings.AUTH_USER_MODEL, verbose_name='Postulante'),
        ),
    ]
