# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-10-13 01:49
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('employer', '0002_auto_20160913_0315'),
    ]

    operations = [
        migrations.CreateModel(
            name='Area',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name=b'Nombre')),
                ('description', models.CharField(max_length=300, verbose_name=b'Descripci\xc3\xb3n')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.IntegerField(choices=[(1, 'Habilitado'), (99, 'Borrador'), (0, 'Pendiente')], default=99)),
                ('title', models.CharField(max_length=100, verbose_name='Puesto / t\xedtulo del aviso')),
                ('reference_number', models.BigIntegerField(blank=True, null=True, verbose_name='N\xfamero de referencia')),
                ('description', models.TextField(verbose_name='Descripci\xf3n del puesto')),
                ('handicapped_postulant', models.BooleanField(default=True, verbose_name='Postulantes discapacitados')),
                ('show_address', models.BooleanField(default=True, verbose_name='Mostrar direcci\xf3n en el aviso')),
                ('get_cvs_ctrl_panel', models.BooleanField(default=True)),
                ('send_cvs_by_mail', models.BooleanField(default=True)),
                ('job_type', models.IntegerField(choices=[(1, 'Full-Time'), (2, 'Part-Time'), (3, 'Freelance')], verbose_name='Tipo de trabajo')),
                ('duration_of_publishing', models.DurationField(default=datetime.timedelta(30))),
                ('featured', models.BooleanField(default=False)),
                ('published', models.DateTimeField(null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('area', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='jobs.Area', verbose_name='Area de publicaci\xf3n')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='jobs', related_query_name='job', to='employer.Employer')),
            ],
        ),
        migrations.CreateModel(
            name='SubArea',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name=b'Nombre')),
                ('description', models.CharField(max_length=300, verbose_name=b'Descripci\xc3\xb3n')),
                ('area', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subareas', to='jobs.Area')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='job',
            name='subarea',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='jobs.SubArea', verbose_name='Sector'),
        ),
    ]
