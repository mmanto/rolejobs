# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-09-04 12:25
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('email', models.EmailField(max_length=255, unique=True, verbose_name='email address')),
                ('username', models.CharField(max_length=1)),
                ('first_name', models.CharField(blank=True, default=None, max_length=250, null=True)),
                ('last_name', models.CharField(blank=True, default=None, max_length=250, null=True)),
                ('city', models.CharField(blank=True, default=None, max_length=250, null=True)),
                ('status', models.SmallIntegerField(default=0)),
                ('is_active', models.BooleanField(default=True)),
                ('is_admin', models.BooleanField(default=False)),
                ('type_profile', models.CharField(choices=[('postulant', 'postulant'), ('employer', 'employer')], max_length=10)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('email_validation_hash', models.CharField(blank=True, default=None, max_length=40, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gender', models.IntegerField(choices=[(0, 'Masculino'), (1, 'Femenino'), (2, 'Otro')], verbose_name='G\xe9nero')),
                ('phone_number', models.CharField(blank=True, max_length=100, verbose_name='Telefono')),
                ('mobile_number', models.CharField(blank=True, max_length=100, verbose_name='Telefono Celular')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('polymorphic_ctype', models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='polymorphic_accounts.profile_set+', to='contenttypes.ContentType')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
