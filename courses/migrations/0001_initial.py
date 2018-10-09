# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2017-02-16 23:23
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import utils.helpers


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Titulo')),
                ('description', models.TextField(verbose_name='Descripci\xf3n')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Precio')),
                ('course_type', models.IntegerField(choices=[(1, 'Distancia'), (2, 'Presencial')], verbose_name='Tipo de curso')),
                ('company_data_from_owner', models.BooleanField(default=True, verbose_name='Datos desde empresa')),
                ('company', models.CharField(blank=True, max_length=255, null=True, verbose_name='Empresa')),
                ('company_logo', models.FileField(blank=True, null=True, upload_to=utils.helpers.get_company_logo_path, verbose_name='Logo de la empresa')),
                ('notify_by_email', models.BooleanField(default=False, verbose_name='Notificaci\xf3n v\xeda email de interesados')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='CoursePostulation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('readed_at', models.DateTimeField()),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.Course')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='coursepostulation',
            unique_together=set([('course', 'user')]),
        ),
    ]
